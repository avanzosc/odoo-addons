/* @odoo-module */

import {
  BankRecKanbanController,
  BankRecKanbanRenderer,
  BankRecKanbanView,
} from "@account_accountant/components/bank_reconciliation/kanban";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {useState} from "@odoo/owl";

export class LegacyBankRecKanbanController extends BankRecKanbanController {
  static template = "account_reconcile_legacy.LegacyBankRecKanbanController";

  setup() {
    super.setup();

    this.legacyUi = useState({
      showOverview: false,
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

  async openRecord(record, mode) {
    // Al pulsar cualquier extracto, volvemos al detalle.
    this.legacyUi.showOverview = false;

    return super.openRecord(record, mode);
  }
  get legacyProgressLabel() {
    const reconciled = this.counter?.count || 0;
    const remaining = this.model?.root?.count || 0;

    return `${reconciled} / ${reconciled + remaining}`;
  }

  get legacyPartnerId() {
    const lines = this.state.bankRecRecordData?.line_ids?.records || [];
    const liquidityLine = lines.find((line) => line.data.flag === "liquidity");
    return liquidityLine?.data.partner_id?.[0] || false;
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
}

export class LegacyBankRecKanbanRenderer extends BankRecKanbanRenderer {
  static template = "account_reconcile_legacy.LegacyBankRecKanbanRenderer";
}

export const LegacyBankRecKanbanView = {
  ...BankRecKanbanView,
  Controller: LegacyBankRecKanbanController,
  Renderer: LegacyBankRecKanbanRenderer,
};

registry
  .category("views")
  .add("legacy_bank_rec_widget_kanban", LegacyBankRecKanbanView);
