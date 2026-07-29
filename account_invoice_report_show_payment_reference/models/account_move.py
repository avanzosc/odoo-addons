# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    print_payment_reference_in_invoices = fields.Boolean(
        string="Print payment reference in invoices",
        compute="_compute_print_reference",
    )

    @api.depends(
        "payment_mode_id", "payment_mode_id.print_payment_reference_in_invoices"
    )
    def _compute_print_reference(self):
        for record in self:
            record.print_payment_reference_in_invoices = (
                record.payment_mode_id.print_payment_reference_in_invoices
                if record.payment_mode_id
                else False
            )
