# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    pending_sale_invoices = fields.Boolean(
        compute="_compute_pending_sale_invoice",
        compute_sudo=True,
    )

    def _compute_pending_sale_invoice(self):
        for record in self:
            pending = False
            if record.sale_id:
                if any(
                    record.mapped("sale_id.invoice_ids").filtered(
                        lambda i: i.state == "posted"
                        and i.payment_state
                        not in ["paid", "reversed", "invoicing_legacy"]
                    )
                ):
                    pending = True
            record.pending_sale_invoices = pending

    def _pre_action_done_hook(self):
        if not self.env.context.get("skip_debt"):
            pickings_to_immediate = self._check_debt()
            if pickings_to_immediate:
                return pickings_to_immediate._action_generate_debt_wizard(
                    show_transfers=self._should_show_transfers()
                )
        return super()._pre_action_done_hook()

    def _check_debt(self):
        debt_pickings = self.browse()
        for picking in self:
            if picking.pending_sale_invoices:
                debt_pickings |= picking
        return debt_pickings

    def _action_generate_debt_wizard(self, show_transfers=False):
        view = self.env.ref("stock_picking_no_debt.stock_debt_transfer_view_form")
        return {
            "name": _("Debt Transfer?"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "stock.debt.transfer",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": dict(
                self.env.context,
                default_show_transfers=show_transfers,
                default_pick_ids=[(4, p.id) for p in self],
            ),
        }
