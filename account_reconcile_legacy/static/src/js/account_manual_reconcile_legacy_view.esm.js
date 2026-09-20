/* @odoo-module */

import {AccountMoveLineListRenderer} from "@account_accountant/components/move_line_list/move_line_list";
import {
  AccountMoveLineReconcileLineListView,
  AccountMoveLineReconcileListController,
} from "@account_accountant/components/move_line_list_reconcile/move_line_list_reconcile";
import {onPatched, useEffect, useState, useSubEnv} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {deserializeDate, formatDate} from "@web/core/l10n/dates";
import {formatMonetary} from "@web/views/fields/formatters";
import {View} from "@web/views/view";

export class LegacyAccountMoveLineReconcileListController extends AccountMoveLineReconcileListController {
  static template =
    "account_reconcile_legacy.LegacyAccountMoveLineReconcileListController";

  setup() {
    super.setup();

    this.orm = useService("orm");

    this.legacyFoldedPairs = useState({
      byAccountId: {},
    });

    this.legacyPairsRequestId = 0;

    useSubEnv({
      legacyFoldedPairs: this.legacyFoldedPairs,

      reconcileLegacySelection: this.reconcileLegacySelection.bind(this),

      reconcileLegacyPair: this.reconcileLegacyPair.bind(this),

      reloadLegacyFoldedPairs: this.loadLegacyFoldedPairs.bind(this),
    });

    useEffect(
      () => {
        this.loadLegacyFoldedPairs();
      },
      () => [
        this.model.root.count,
        JSON.stringify(this.model.root.domain || []),
        this.legacyVisibleAccountIds.join(","),
        this.legacyGroupPageKey,
      ]
    );
  }

  get legacyVisibleAccountIds() {
    const accountIds = (this.model.root.groups || [])
      .map((group) => group.list?.evalContext?.default_account_id)
      .map((value) => (Array.isArray(value) ? value[0] : value))
      .filter(Boolean);

    return [...new Set(accountIds)];
  }

  get legacyGroupPageKey() {
    return (this.model.root.groups || [])
      .filter((group) => group.count > 0)
      .map((group) => {
        const value = group.list?.evalContext?.default_account_id;

        const accountId = Array.isArray(value) ? value[0] : value;

        const offset = Number(group.list?.offset || 0);

        const limit = Number(group.list?.limit || 80);

        return `${accountId || 0}:${offset}:${limit}`;
      })
      .join("|");
  }

  async loadLegacyFoldedPairs() {
    const accountIds = this.legacyVisibleAccountIds;

    const requestId = ++this.legacyPairsRequestId;

    if (!accountIds.length) {
      return;
    }

    const lines = await this.orm.searchRead(
      "account.move.line",
      [...(this.model.root.domain || []), ["account_id", "in", accountIds]],
      [
        "account_id",
        "company_id",
        "company_currency_id",
        "partner_id",
        "move_name",
        "name",
        "ref",
        "date",
        "debit",
        "credit",
        "amount_residual",
      ],
      {
        order: "account_id, date desc, id desc",
      }
    );

    if (requestId !== this.legacyPairsRequestId) {
      return;
    }

    const linesByAccount = new Map();

    for (const line of lines) {
      const accountId = line.account_id?.[0];

      if (!accountId) {
        continue;
      }

      const accountLines = linesByAccount.get(accountId) || [];

      accountLines.push(line);

      linesByAccount.set(accountId, accountLines);
    }

    const visibleLines = [];

    for (const group of this.model.root.groups || []) {
      if (!group.count) {
        continue;
      }

      const value = group.list?.evalContext?.default_account_id;

      const accountId = Array.isArray(value) ? value[0] : value;

      if (!accountId) {
        continue;
      }

      const accountLines = linesByAccount.get(accountId) || [];

      const offset = Number(group.list?.offset || 0);

      const limit = Number(group.list?.limit || 80);

      visibleLines.push(...accountLines.slice(offset, offset + limit));
    }

    this.legacyFoldedPairs.byAccountId = this.buildLegacyBalancedPairs(visibleLines);
  }

  getLegacyExactPairAmount(line) {
    const debit = Number(line.debit || 0);

    const credit = Number(line.credit || 0);

    const originalAmount = debit - credit;

    const residual = Number(line.amount_residual || 0);

    const tolerance = 0.00001;

    if (Math.abs(originalAmount) < tolerance) {
      return 0;
    }

    if (Math.abs(originalAmount - residual) >= tolerance) {
      return 0;
    }

    return originalAmount;
  }

  buildLegacyBalancedPairs(lines) {
    const pendingLines = new Map();

    const pairsByAccount = {};

    for (const line of lines) {
      const accountId = line.account_id?.[0];

      const companyId = line.company_id?.[0] || 0;

      const currencyId = line.company_currency_id?.[0] || 0;

      const amount = this.getLegacyExactPairAmount(line);

      if (!accountId || pairsByAccount[accountId] || !amount) {
        continue;
      }

      const sign = amount > 0 ? 1 : -1;

      const amountKey = Math.abs(amount).toFixed(6);

      const commonKey = [accountId, companyId, currencyId, amountKey].join(":");

      const currentKey = `${commonKey}:${sign}`;

      const oppositeKey = `${commonKey}:${-sign}`;

      const oppositeLines = pendingLines.get(oppositeKey) || [];

      if (oppositeLines.length) {
        const oppositeLine = oppositeLines.pop();

        const pairLines = [oppositeLine, line].sort(
          (first, second) => Number(second.debit || 0) - Number(first.debit || 0)
        );

        pairsByAccount[accountId] = {
          account_id: accountId,

          line_ids: pairLines.map((pairLine) => pairLine.id),

          lines: pairLines,
        };

        continue;
      }

      const currentLines = pendingLines.get(currentKey) || [];

      currentLines.push(line);

      pendingLines.set(currentKey, currentLines);
    }

    return pairsByAccount;
  }

  async reconcileLegacyPair(pair) {
    const resIds = pair?.line_ids || [];

    if (resIds.length < 2) {
      return;
    }

    await this.actionService.doActionButton({
      name: "action_reconcile",
      type: "object",
      resModel: this.props.resModel,
      resIds,
      context: {
        ...this.props.context,
        active_model: this.props.resModel,
        active_ids: resIds,
      },
      onClose: async () => {
        await this.model.load();
        await this.loadLegacyFoldedPairs();
      },
    });

    await this.model.load();
    await this.loadLegacyFoldedPairs();
  }

  get legacyProgressLabel() {
    const remaining = this.model?.root?.count || 0;
    return `0 / ${remaining}`;
  }

  async reconcileLegacySelection() {
    const records = [...this.model.root.selection];

    if (records.length < 2) {
      return;
    }

    const balance = records.reduce(
      (total, record) =>
        total + Number(record.data.amount_residual ?? record.data.balance ?? 0),
      0
    );

    if (Math.abs(balance) >= 0.00001) {
      return;
    }

    const resIds = records.map((record) => record.resId);

    await this.actionService.doActionButton({
      name: "action_reconcile",
      type: "object",
      resModel: this.props.resModel,
      resIds,
      context: {
        ...this.props.context,
        active_model: this.props.resModel,
        active_ids: resIds,
      },
      onClose: () => this.model.load(),
    });

    await this.model.load();
  }
}

export class LegacyAccountMoveLineReconcileListRenderer extends AccountMoveLineListRenderer {
  static components = {
    ...AccountMoveLineListRenderer.components,
    View,
  };

  static rowsTemplate = "account_reconcile_legacy.LegacyAccountMoveLineReconcileRows";

  static recordRowTemplate =
    "account_reconcile_legacy.LegacyAccountMoveLineReconcileRecordRow";

  static groupRowTemplate =
    "account_reconcile_legacy.LegacyAccountMoveLineReconcileGroupRow";

  setup() {
    super.setup();
    this.orm = useService("orm");
    this.legacyUi = useState({
      candidateFilter: "",
      writeoffOpen: false,
      writeoffGroupId: false,
      writeoffWizardId: false,
      writeoffViewId: false,
    });

    this.suggestedGroupSignatures = new Map();

    useEffect(
      () => {
        this.openFirstGroupAndLoadFoldedPairs();
      },
      () => [this.visibleGroups[0]?.id]
    );

    onPatched(() => {
      if (this.activeGroup) {
        this.suggestBalancedPair();
      }
    });
  }

  closeLegacyWriteoff() {
    this.legacyUi.writeoffOpen = false;
    this.legacyUi.writeoffGroupId = false;
    this.legacyUi.writeoffWizardId = false;
    this.legacyUi.writeoffViewId = false;
  }

  getLegacyExactProposalAmount(record) {
    const data = record.data;

    const debit = Number(data.debit || 0);

    const credit = Number(data.credit || 0);

    const originalAmount = debit - credit;

    const residual = Number(data.amount_residual || 0);

    const tolerance = 0.00001;

    if (Math.abs(originalAmount) < tolerance) {
      return 0;
    }

    if (Math.abs(originalAmount - residual) >= tolerance) {
      return 0;
    }

    return originalAmount;
  }

  async toggleLegacyWriteoff(group) {
    if (this.legacyUi.writeoffOpen && this.legacyUi.writeoffGroupId === group.id) {
      this.closeLegacyWriteoff();
      return;
    }

    const records = this.getGroupProposedRecords(group);
    const resIds = records.map((record) => record.resId);

    if (!resIds.length) {
      return;
    }

    const result = await this.orm.call(
      "account.reconcile.legacy.writeoff",
      "create_from_lines",
      [resIds]
    );

    this.legacyUi.writeoffWizardId = result.wizard_id;

    this.legacyUi.writeoffViewId = result.view_id;

    this.legacyUi.writeoffGroupId = group.id;
    this.legacyUi.writeoffOpen = true;
  }

  async openFirstGroupAndLoadFoldedPairs() {
    const firstGroup = this.visibleGroups[0];

    if (!firstGroup) {
      return;
    }

    if (firstGroup.isFolded) {
      await this.toggleGroup(firstGroup);
    }

    await this.env.reloadLegacyFoldedPairs();

    this.render();
  }

  getLegacyGroupAccountId(group) {
    const value = group.list?.evalContext?.default_account_id;

    return Array.isArray(value) ? value[0] : value;
  }

  getFoldedGroupPair(group) {
    if (!group.isFolded) {
      return false;
    }

    const accountId = this.getLegacyGroupAccountId(group);

    return this.env.legacyFoldedPairs?.byAccountId?.[accountId] || false;
  }

  getLegacyFoldedDescription(line) {
    const values = [line.partner_id?.[1], line.move_name, line.name, line.ref];

    const parts = [];
    const normalizedParts = new Set();

    for (const value of values) {
      const normalizedValue = String(value || "")
        .replace(/\s+/g, " ")
        .trim();
      const normalizedKey = normalizedValue.toLocaleLowerCase();

      if (normalizedValue && !normalizedParts.has(normalizedKey)) {
        parts.push(normalizedValue);
        normalizedParts.add(normalizedKey);
      }
    }

    return parts.join(": ");
  }

  getLegacyFoldedDate(line) {
    if (!line.date) {
      return "";
    }

    return formatDate(deserializeDate(line.date));
  }

  getLegacyFoldedAmount(line, fieldName) {
    return formatMonetary(Number(line[fieldName] || 0), {
      currencyId: line.company_currency_id?.[0],
    });
  }

  getLegacyAmlDescription(record) {
    const data = record.data;
    const values = [
      Array.isArray(data.partner_id) ? data.partner_id[1] : "",
      data.move_name,
      data.name,
      data.ref,
    ];

    const parts = [];

    for (const value of values) {
      const normalizedValue = String(value || "")
        .replace(/\s+/g, " ")
        .trim();

      const alreadyIncluded = parts.some(
        (part) => part.toLocaleLowerCase() === normalizedValue.toLocaleLowerCase()
      );

      if (normalizedValue && !alreadyIncluded) {
        parts.push(normalizedValue);
      }
    }

    return parts.join(": ");
  }

  getLegacyFormattedValue(record, fieldName) {
    const column = this.getColumns(record).find(
      (candidateColumn) =>
        candidateColumn.type === "field" && candidateColumn.name === fieldName
    );

    if (column && this.canUseFormatter(column, record)) {
      return this.getFormattedValue(column, record);
    }

    return this.getSearchableValue(record.data[fieldName]);
  }

  get visibleGroups() {
    return this.props.list.groups?.filter((group) => group.count > 0) || [];
  }

  get activeGroup() {
    return this.visibleGroups.find((group) => !group.isFolded) || null;
  }

  getGroupSignature(group) {
    return group.list.records.map((record) => record.resId).join(",");
  }

  suggestBalancedPair() {
    const group = this.activeGroup;

    if (!group || !group.list.records.length) {
      return;
    }

    const signature = this.getGroupSignature(group);

    if (this.suggestedGroupSignatures.get(group.id) === signature) {
      return;
    }

    this.suggestedGroupSignatures.set(group.id, signature);

    if (group.list.records.some((record) => record.selected)) {
      return;
    }

    const records = group.list.records;

    for (let firstIndex = 0; firstIndex < records.length; firstIndex++) {
      const firstRecord = records[firstIndex];

      const firstAmount = this.getLegacyExactProposalAmount(firstRecord);

      if (!firstAmount) {
        continue;
      }

      for (
        let secondIndex = firstIndex + 1;
        secondIndex < records.length;
        secondIndex++
      ) {
        const secondRecord = records[secondIndex];

        const secondAmount = this.getLegacyExactProposalAmount(secondRecord);

        if (!secondAmount) {
          continue;
        }

        if (
          Math.sign(firstAmount) !== Math.sign(secondAmount) &&
          Math.abs(firstAmount + secondAmount) < 0.00001
        ) {
          firstRecord.toggleSelection(true);

          secondRecord.toggleSelection(true);

          return;
        }
      }
    }
  }

  getResidualAmount(record) {
    const residual = record.data.amount_residual;

    if (typeof residual === "number") {
      return residual;
    }

    return Number(record.data.balance || 0);
  }

  getGroupProposedRecords(group) {
    return group.list.records.filter((record) => record.selected);
  }

  getGroupAvailableRecords(group) {
    return group.list.records.filter((record) => !record.selected);
  }

  getGroupCandidateRecords(group) {
    const availableRecords = this.getGroupAvailableRecords(group);
    const filter = this.legacyUi.candidateFilter.trim().toLowerCase();

    if (!filter) {
      return availableRecords;
    }

    return availableRecords.filter((record) => {
      const data = record.data;
      const searchableValues = [
        data.account_id,
        data.partner_id,
        data.date,
        data.move_name,
        data.ref,
        data.name,
        data.debit,
        data.credit,
        data.amount_residual,
      ];

      return searchableValues
        .map((value) => this.getSearchableValue(value))
        .join(" ")
        .toLowerCase()
        .includes(filter);
    });
  }

  onLegacyLineKeydown(ev, record) {
    if (ev.key !== "Enter" && ev.key !== " ") {
      return;
    }

    ev.preventDefault();
    this.toggleRecordSelection(record);
  }

  getSearchableValue(value) {
    if (Array.isArray(value)) {
      return value[1] || "";
    }

    return String(value ?? "");
  }

  canReconcileGroup(group) {
    const proposedRecords = this.getGroupProposedRecords(group);

    if (proposedRecords.length < 2) {
      return false;
    }

    const balance = this.getLegacySelectionBalance(group);

    return Math.abs(balance) < 0.00001;
  }

  updateCandidateFilter(ev) {
    this.legacyUi.candidateFilter = ev.target.value;
  }

  async clearLegacySelection() {
    const selectedRecords = [...this.props.list.selection];

    for (const record of selectedRecords) {
      await record.toggleSelection(false);
    }
  }

  async onGroupHeaderClicked(ev, group) {
    const left = await this.props.list.leaveEditMode();

    if (!left) {
      return;
    }

    const foldedPair = group.isFolded ? this.getFoldedGroupPair(group) : false;

    await this.clearLegacySelection();

    for (const openGroup of this.visibleGroups) {
      if (openGroup !== group && !openGroup.isFolded) {
        await openGroup.toggle();
      }
    }

    this.legacyUi.candidateFilter = "";

    this.legacyUi.writeoffOpen = false;

    this.legacyUi.writeoffGroupId = false;

    this.suggestedGroupSignatures.delete(group.id);

    await group.toggle();

    if (foldedPair && !group.isFolded) {
      const pairIds = new Set(foldedPair.line_ids.map((id) => Number(id)));

      const pairRecords = group.list.records.filter((record) =>
        pairIds.has(Number(record.resId))
      );

      if (pairRecords.length === pairIds.size) {
        for (const record of pairRecords) {
          if (!record.selected) {
            await record.toggleSelection(true);
          }
        }

        this.suggestedGroupSignatures.set(group.id, this.getGroupSignature(group));
      }
    }
  }

  getLegacySelectionBalance(group) {
    return this.getGroupProposedRecords(group).reduce(
      (total, record) => total + this.getResidualAmount(record),
      0
    );
  }

  getLegacySelectionCurrencyId(group) {
    const record = this.getGroupProposedRecords(group)[0];

    return record?.data.company_currency_id?.[0] || false;
  }

  formatLegacySelectionAmount(group, amount) {
    if (!amount) {
      return "";
    }

    return formatMonetary(Math.abs(amount), {
      currencyId: this.getLegacySelectionCurrencyId(group),
    });
  }

  getLegacyWriteoffDebit(group) {
    const balance = this.getLegacySelectionBalance(group);

    return balance < -0.000001 ? this.formatLegacySelectionAmount(group, balance) : "";
  }

  getLegacyWriteoffCredit(group) {
    const balance = this.getLegacySelectionBalance(group);

    return balance > 0.000001 ? this.formatLegacySelectionAmount(group, balance) : "";
  }

  hasLegacyWriteoffBalance(group) {
    return Math.abs(this.getLegacySelectionBalance(group)) > 0.000001;
  }
  getLegacyWriteoffFormProps(group) {
    const records = this.getGroupProposedRecords(group);

    const viewId = this.legacyUi.writeoffViewId;

    return {
      type: "form",

      resModel: "account.reconcile.legacy.writeoff",

      resId: this.legacyUi.writeoffWizardId,

      viewId,

      views: [[viewId, "form"]],

      mode: "edit",

      preventCreate: true,

      context: {
        ...this.props.context,

        active_model: "account.move.line",

        active_ids: records.map((record) => record.resId),
      },

      display: {
        controlPanel: false,
      },

      searchMenuTypes: [],
    };
  }
}

export const LegacyAccountMoveLineReconcileListView = {
  ...AccountMoveLineReconcileLineListView,
  Controller: LegacyAccountMoveLineReconcileListController,
  Renderer: LegacyAccountMoveLineReconcileListRenderer,
};

registry
  .category("views")
  .add(
    "legacy_account_move_line_reconcile_list",
    LegacyAccountMoveLineReconcileListView
  );
