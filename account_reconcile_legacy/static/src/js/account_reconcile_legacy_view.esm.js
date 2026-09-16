/* @odoo-module */

import {Many2OneField} from "@web/views/fields/many2one/many2one_field";
import {useService} from "@web/core/utils/hooks";
import {
  BankRecKanbanController,
  BankRecKanbanRenderer,
  BankRecKanbanView,
} from "@account_accountant/components/bank_reconciliation/kanban";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {onMounted, onPatched, useEffect, useRef, useState, useSubEnv} from "@odoo/owl";
import {formatDate} from "@web/core/l10n/dates";
import {formatMonetary} from "@web/views/fields/formatters";

export class LegacyBankRecKanbanController extends BankRecKanbanController {
  static template = "account_reconcile_legacy.LegacyBankRecKanbanController";

  setup() {
    super.setup();

    useSubEnv({
      legacyBankRecController: this,
    });

    this.legacyUi = useState({
      showOverview: false,
      inlinePortalReady: false,
      activeRecordId: false,
      openingRecord: false,
    });
    this.legacyPrepared = useState({
      byStatementId: {},
    });

    this._legacyPreparingProposals = false;

    useEffect(
      () => {
        if (this.legacyUi.openingRecord) {
          return;
        }

        const loadedRecordId = Number(this.state.bankRecStLineId);

        const activeRecordId = Number(this.legacyUi.activeRecordId);

        if (!loadedRecordId || loadedRecordId !== activeRecordId) {
          return;
        }

        const manualLine = this.legacyManualEditLine;

        if (!manualLine) {
          return;
        }

        void this.syncLegacyPartnerToManualLine(manualLine);
      },
      () => [
        this.legacyPartnerId,
        this.state.bankRecRecordData?.form_index,
        this.state.bankRecStLineId,
        this.state.bankRecNotebookPage,
        this.legacyUi.activeRecordId,
        this.legacyUi.openingRecord,
      ]
    );
  }

  getLegacyBackupValues(state = this.state) {
    return Object.assign({}, state.bankRecEmbeddedViewsData || {}, {
      bankRecStLineId: state.bankRecStLineId,

      initial_values: this.bankRecModel.getInitialValues(),
    });
  }

  async prepareLegacyProposals(proposals) {
    if (this._legacyPreparingProposals || !this.bankRecModel) {
      return;
    }

    const entries = Object.entries(proposals || {}).filter(
      ([, proposal]) => proposal?.id
    );

    if (!entries.length) {
      return;
    }

    this._legacyPreparingProposals = true;

    const previousOpeningRecord = this.legacyUi.openingRecord;

    this.legacyUi.openingRecord = true;
    this.legacyUi.inlinePortalReady = false;

    await new Promise((resolve) => {
      browser.requestAnimationFrame(resolve);
    });

    try {
      const originalStLineId = this.state.bankRecStLineId;

      const originalBackup = originalStLineId ? this.getLegacyBackupValues() : false;

      const prepared = {
        ...this.legacyPrepared.byStatementId,
      };

      await this.execProtectedBankRecAction(async () => {
        for (const [statementIdString, proposal] of entries) {
          const statementId = Number(statementIdString);

          if (prepared[statementIdString]?.amlId === proposal.id) {
            continue;
          }

          await this.withNewState(async (newState) => {
            await this._mountStLineInEdit(newState, statementId);
          });

          if (Number(this.state.bankRecStLineId) !== statementId) {
            continue;
          }

          let lines = this.state.bankRecRecordData?.line_ids?.records || [];

          const alreadySelected = lines.some(
            (line) =>
              line.data.flag === "new_aml" &&
              Number(line.data.source_aml_id?.[0] || 0) === Number(proposal.id)
          );

          if (!alreadySelected) {
            await this.withNewState(async (newState) => {
              await this.onchange(newState, "add_new_aml", [proposal.id]);
            });
          }

          const data = this.state.bankRecRecordData;

          if (Number(this.state.bankRecStLineId) !== statementId) {
            continue;
          }

          lines = data?.line_ids?.records || [];

          const autoBalanceLine =
            lines.find((line) => line.data.flag === "auto_balance") || false;

          const hasCounterpart = lines.some(
            (line) =>
              line.data.flag !== "liquidity" && line.data.flag !== "auto_balance"
          );

          const hasProposalAml = lines.some(
            (line) =>
              line.data.flag === "new_aml" &&
              Number(line.data.source_aml_id?.[0] || 0) === Number(proposal.id)
          );

          prepared[statementIdString] = {
            amlId: proposal.id,

            backup: this.getLegacyBackupValues(),

            state: data?.state || false,

            areAllLinesValid: data ? this.checkBankRecLinesInvalidFields(data) : false,

            hasCounterpart,

            hasProposalAml,

            residualDebit: Number(autoBalanceLine?.data?.debit || 0),

            residualCredit: Number(autoBalanceLine?.data?.credit || 0),
          };
        }

        if (originalStLineId) {
          const preparedOriginal = prepared[String(originalStLineId)];

          await this.withNewState(async (newState) => {
            await this._mountStLineInEdit(
              newState,
              originalStLineId,
              preparedOriginal?.backup || originalBackup
            );
          });
        }
      });

      this.legacyPrepared.byStatementId = prepared;
    } finally {
      this._legacyPreparingProposals = false;

      this.legacyUi.openingRecord = previousOpeningRecord;
    }
  }

  getLegacyPreparedState(statementId) {
    return this.legacyPrepared.byStatementId?.[String(statementId)] || false;
  }

  get legacyActiveRecordId() {
    return this.legacyUi.activeRecordId || this.state.bankRecStLineId || false;
  }

  get legacyLiquidityLine() {
    const lines = this.state.bankRecRecordData?.line_ids?.records || [];

    return lines.find((line) => line.data.flag === "liquidity") || false;
  }

  get legacyManualEditLine() {
    const data = this.state.bankRecRecordData;

    if (!data) {
      return false;
    }

    if (this.state.bankRecNotebookPage !== "manual_operations_tab") {
      return false;
    }

    const formIndex = data.form_index;

    if (formIndex === undefined || formIndex === null) {
      return false;
    }

    return (
      data.line_ids.records.find(
        (line) => line.data.index === formIndex && line.data.flag !== "liquidity"
      ) || false
    );
  }

  async syncLegacyPartnerToManualLine(line) {
    if (!line) {
      return;
    }

    const liquidityLine = this.legacyLiquidityLine;

    if (!liquidityLine) {
      return;
    }

    const partner = liquidityLine.data.partner_id || false;

    const partnerId = partner?.[0] || false;

    const currentPartnerId = line.data.partner_id?.[0] || false;

    if (partnerId === currentPartnerId) {
      return;
    }

    await line.update({
      partner_id: partner,
    });
  }

  get legacyPartnerId() {
    return this.legacyLiquidityLine?.data.partner_id?.[0] || false;
  }

  get legacyAmlListKey() {
    return `${this.state.bankRecStLineId || 0}-${this.legacyPartnerId || 0}`;
  }

  notebookAmlsListViewProps() {
    const props = super.notebookAmlsListViewProps();

    const partnerId = this.legacyPartnerId;

    if (!partnerId) {
      return props;
    }

    return {
      ...props,
      domain: [...props.domain, ["partner_id", "=", partnerId]],
    };
  }

  async actionAddNewAml(amlId) {
    await this.execProtectedBankRecAction(async () => {
      await this.withNewState(async (newState) => {
        await this.onchange(newState, "add_new_aml_legacy", [amlId]);
      });
    });
  }

  async actionRemoveNewAml(amlId) {
    await this.execProtectedBankRecAction(async () => {
      await this.withNewState(async (newState) => {
        await this.onchange(newState, "remove_new_aml_legacy", [amlId]);
      });
    });
  }

  async actionRemoveLine(line) {
    const wasManualTab = this.state.bankRecNotebookPage === "manual_operations_tab";

    await this.execProtectedBankRecAction(async () => {
      await this.withNewState(async (newState) => {
        await this.onchange(newState, "remove_line_legacy", [line.data.index]);
      });

      if (!wasManualTab) {
        return;
      }

      const data = this.state.bankRecRecordData;

      const autoBalanceLine = data?.line_ids?.records?.find(
        (currentLine) => currentLine.data.flag === "auto_balance"
      );

      if (!autoBalanceLine) {
        return;
      }

      await this.withNewState(async (newState) => {
        await this._actionMountLineInEdit(newState, autoBalanceLine);
      });
    });
  }

  toggleLegacyOverview() {
    this.legacyUi.showOverview = !this.legacyUi.showOverview;

    browser.requestAnimationFrame(() => {
      this.viewRef.el?.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  async openRecord(record) {
    const recordId = record.resId || false;

    if (!recordId) {
      return;
    }

    this.legacyUi.showOverview = false;

    this.legacyUi.inlinePortalReady = false;

    this.legacyUi.openingRecord = true;

    try {
      const currentStLineId = this.bankRecModel?.root?.data?.st_line_id?.[0] || false;

      if (Number(currentStLineId) === Number(recordId)) {
        this.legacyUi.activeRecordId = recordId;

        return;
      }

      const prepared = this.getLegacyPreparedState(recordId);

      await this.execProtectedAction(async () => {
        await this.withNewState(async (newState) => {
          await this._mountStLineInEdit(newState, recordId, prepared?.backup || null);
        });
      });

      this.legacyUi.activeRecordId = recordId;
    } finally {
      this.legacyUi.openingRecord = false;
    }
  }

  get legacyProgressLabel() {
    const reconciled = this.counter?.count || 0;

    const remaining = this.model?.root?.count || 0;

    return `${reconciled} / ${reconciled + remaining}`;
  }
}

export class LegacyBankRecKanbanRenderer extends BankRecKanbanRenderer {
  static template = "account_reconcile_legacy.LegacyBankRecKanbanRenderer";

  static components = {
    ...BankRecKanbanRenderer.components,
    Many2OneField,
  };

  setup() {
    super.setup();
    this.orm = useService("orm");

    this.legacyProposals = useState({
      byStatementId: {},
    });
    this.legacyUi = useState(this.env.legacyBankRecController.legacyUi);

    this.legacyState = useState(this.env.legacyBankRecController.state);

    this.rootRef = useRef("root");
    this._legacyExpandingGroups = false;

    useEffect(
      () => {
        void this.loadLegacyExactProposals();
      },
      () => [this.getLegacyStatementIdsKey()]
    );

    onMounted(() => {
      void this.expandLegacyStatementGroups().then(() => {
        this.syncLegacyInlinePortal();
      });
    });

    onPatched(() => {
      this.syncLegacyInlinePortal();

      void this.expandLegacyStatementGroups().then(() => {
        this.syncLegacyInlinePortal();
      });
    });
  }

  getLegacyStatementRecords() {
    const records = [];

    for (const groupOrRecord of this.getGroupsOrRecords()) {
      if (groupOrRecord.group) {
        records.push(...(groupOrRecord.group.list?.records || []));
      } else if (groupOrRecord.record) {
        records.push(groupOrRecord.record);
      }
    }

    return records;
  }

  getLegacyStatementIdsKey() {
    return this.getLegacyStatementRecords()
      .map((record) => record.resId)
      .filter(Boolean)
      .join(",");
  }

  async loadLegacyExactProposals() {
    const statementIds = this.getLegacyStatementRecords()
      .map((record) => record.resId)
      .filter(Boolean);

    if (!statementIds.length) {
      return;
    }

    const proposals = await this.orm.call(
      "account.bank.statement.line",
      "get_legacy_exact_match_proposals",
      [statementIds]
    );

    this.legacyProposals.byStatementId = proposals || {};
  }

  getLegacyProposal(record) {
    const proposal = this.legacyProposals.byStatementId?.[String(record.resId)];

    if (!proposal) {
      return false;
    }

    if (this.isLegacyActiveRecord(record)) {
      const lines =
        this.legacyController.state.bankRecRecordData?.line_ids?.records || [];

      const hasSelectedLines = lines.some(
        (line) => line.data.flag !== "liquidity" && line.data.flag !== "auto_balance"
      );

      if (hasSelectedLines) {
        return false;
      }
    }

    return proposal;
  }

  formatLegacyProposalAmount(proposal, field) {
    const amount = Number(proposal?.[field] || 0);

    if (!amount) {
      return "";
    }

    return formatMonetary(amount, {
      currencyId: proposal.currency_id || false,
    });
  }

  get legacyController() {
    return this.env.legacyBankRecController;
  }

  get legacyActiveRecordId() {
    return (
      this.legacyUi.activeRecordId ||
      this.legacyController.state.bankRecStLineId ||
      false
    );
  }

  get legacyAutoBalanceLine() {
    const lines = this.legacyState?.bankRecRecordData?.line_ids?.records || [];

    return lines.find((line) => line.data.flag === "auto_balance") || false;
  }

  getLegacyHintDebit(record) {
    if (this.isLegacyActiveRecord(record)) {
      const line = this.legacyAutoBalanceLine;

      if (!line) {
        return "";
      }

      const amount = Number(line.data.debit || 0);

      if (!amount) {
        return "";
      }

      return formatMonetary(amount, {
        currencyId: line.data.company_currency_id?.[0] || false,
      });
    }

    const prepared = this.getLegacyPreparedState(record);

    if (prepared && prepared.hasProposalAml) {
      const amount = Number(prepared.residualDebit || 0);

      if (!amount) {
        return "";
      }

      return formatMonetary(amount, {
        currencyId: this.getLegacyStatementCurrencyId(record),
      });
    }

    return this.getLegacyStatementCredit(record);
  }

  getLegacyHintCredit(record) {
    if (this.isLegacyActiveRecord(record)) {
      const line = this.legacyAutoBalanceLine;

      if (!line) {
        return "";
      }

      const amount = Number(line.data.credit || 0);

      if (!amount) {
        return "";
      }

      return formatMonetary(amount, {
        currencyId: line.data.company_currency_id?.[0] || false,
      });
    }

    const prepared = this.getLegacyPreparedState(record);

    if (prepared && prepared.hasProposalAml) {
      const amount = Number(prepared.residualCredit || 0);

      if (!amount) {
        return "";
      }

      return formatMonetary(amount, {
        currencyId: this.getLegacyStatementCurrencyId(record),
      });
    }

    return this.getLegacyStatementDebit(record);
  }

  async applyLegacyProposalToActiveRecord(record) {
    const controller = this.legacyController;

    const proposal = this.legacyProposals.byStatementId?.[String(record.resId)];

    if (!controller || !proposal) {
      return false;
    }

    if (Number(controller.state.bankRecStLineId) !== Number(record.resId)) {
      return false;
    }

    const lines = controller.state.bankRecRecordData?.line_ids?.records || [];

    const alreadySelected = lines.some(
      (line) =>
        line.data.flag === "new_aml" &&
        Number(line.data.source_aml_id?.[0] || 0) === Number(proposal.id)
    );

    if (!alreadySelected) {
      await controller.actionAddNewAml(proposal.id);
    }

    return true;
  }

  async openLegacyRecord(record) {
    const controller = this.legacyController;

    if (!controller) {
      return;
    }

    await controller.openRecord(record);

    await this.applyLegacyProposalToActiveRecord(record);

    await new Promise((resolve) => {
      browser.requestAnimationFrame(resolve);
    });

    this.syncLegacyInlinePortal();
  }

  async validateLegacyRecord(record) {
    const controller = this.legacyController;

    if (!controller) {
      return;
    }

    if (!this.isLegacyActiveRecord(record)) {
      await controller.openRecord(record);
    }

    await this.applyLegacyProposalToActiveRecord(record);

    const data = controller.state.bankRecRecordData;

    if (!data || data.state !== "valid") {
      return;
    }

    const areAllLinesValid = controller.checkBankRecLinesInvalidFields(data);

    if (!areAllLinesValid) {
      return;
    }

    await controller.actionValidate();
  }

  getLegacyPreparedState(record) {
    return this.legacyController.getLegacyPreparedState(record.resId);
  }

  isLegacyActiveRecord(record) {
    if (this.legacyUi.showOverview) {
      return false;
    }

    const recordId = Number(record.resId);

    const activeRecordId = Number(this.legacyActiveRecordId);

    const loadedRecordId = Number(this.legacyController.state.bankRecStLineId);

    return recordId === activeRecordId && recordId === loadedRecordId;
  }

  async toggleLegacyRecord(record) {
    const controller = this.legacyController;

    if (!controller) {
      return;
    }

    const recordId = Number(record.resId);

    const activeRecordId = Number(controller.legacyActiveRecordId);

    const isOpen = !controller.legacyUi.showOverview && recordId === activeRecordId;

    if (isOpen) {
      controller.legacyUi.inlinePortalReady = false;

      controller.legacyUi.showOverview = true;

      return;
    }
    await this.openLegacyRecord(record);
  }

  async updateLegacyStatementPartner(record, changes) {
    await record.update(changes);

    await this.openLegacyRecord(record);

    const controller = this.legacyController;

    if (!controller) {
      return;
    }

    const liquidityLine = controller.legacyLiquidityLine;

    if (!liquidityLine) {
      return;
    }

    const partner = record.data.partner_id || false;

    const currentPartner = liquidityLine.data.partner_id || false;

    if ((partner?.[0] || false) !== (currentPartner?.[0] || false)) {
      await liquidityLine.update({
        partner_id: partner,
      });
    }

    const manualLine = controller.legacyManualEditLine;

    if (manualLine) {
      await controller.syncLegacyPartnerToManualLine(manualLine);
    }
  }

  syncLegacyInlinePortal() {
    const controller = this.legacyController;

    if (!controller) {
      return;
    }

    if (this.legacyUi.openingRecord) {
      return;
    }

    const stLineId = this.legacyActiveRecordId;

    if (!stLineId) {
      if (this.legacyUi.inlinePortalReady) {
        this.legacyUi.inlinePortalReady = false;
      }

      return;
    }

    const root = this.rootRef.el;

    if (!root) {
      return;
    }

    const linesTarget = root.querySelector(
      `#o_legacy_inline_bank_rec_lines_${stLineId}`
    );

    const detailsTarget = root.querySelector(
      `#o_legacy_inline_bank_rec_details_${stLineId}`
    );

    const ready = Boolean(linesTarget && detailsTarget);

    if (this.legacyUi.inlinePortalReady !== ready) {
      this.legacyUi.inlinePortalReady = ready;
    }
  }

  formatLegacyStatementDate(record) {
    const date = record.data.date;

    return date ? formatDate(date) : "";
  }

  getLegacyStatementCode(record) {
    return record.data.legacy_liquidity_account_code || "";
  }

  getLegacyStatementLabel(record) {
    return record.data.payment_ref || record.data.name || record.data.ref || "";
  }

  getLegacyStatementAmount(record) {
    return Number(record.data.amount || 0);
  }

  getLegacyStatementCurrencyId(record) {
    return (
      record.data.currency_id?.[0] || record.data.company_currency_id?.[0] || false
    );
  }

  formatLegacyStatementAmount(record) {
    const amount = Math.abs(this.getLegacyStatementAmount(record));

    if (!amount) {
      return "";
    }

    return formatMonetary(amount, {
      currencyId: this.getLegacyStatementCurrencyId(record),
    });
  }

  getLegacyStatementDebit(record) {
    const amount = this.getLegacyStatementAmount(record);

    return amount > 0 ? this.formatLegacyStatementAmount(record) : "";
  }

  getLegacyStatementCredit(record) {
    const amount = this.getLegacyStatementAmount(record);

    return amount < 0 ? this.formatLegacyStatementAmount(record) : "";
  }

  async expandLegacyStatementGroups() {
    if (this._legacyExpandingGroups) {
      return;
    }

    const list = this.props.list;

    if (!list?.isGrouped) {
      return;
    }

    const foldedGroups = list.groups?.filter((group) => group.isFolded) || [];

    if (!foldedGroups.length) {
      return;
    }

    this._legacyExpandingGroups = true;

    try {
      for (const group of foldedGroups) {
        if (group.isFolded) {
          await group.toggle();
        }
      }
    } finally {
      this._legacyExpandingGroups = false;
    }
  }
}

export const LegacyBankRecKanbanView = {
  ...BankRecKanbanView,
  Controller: LegacyBankRecKanbanController,
  Renderer: LegacyBankRecKanbanRenderer,
};

registry
  .category("views")
  .add("legacy_bank_rec_widget_kanban", LegacyBankRecKanbanView);
