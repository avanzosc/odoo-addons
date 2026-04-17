# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


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

    def button_validate(self):
        if any(self.mapped("pending_sale_invoices")):
            raise UserError(_("You can not validate picking with pending invoices."))
        return super().button_validate()
