# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("invoice_date", "company_id")
    def _compute_date(self):
        if self.env.context.get("create_bill", False) or self.env.context.get(
            "auditlog_disabled", False
        ):
            return super()._compute_date()
        result = True
        supplier_moves = self.filtered(
            lambda x: x.move_type in ("in_invoice", "in_refund")
        )
        other_moves = self - supplier_moves
        if other_moves:
            result = super(AccountMove, other_moves)._compute_date()
        for move in supplier_moves:
            move.date = move.invoice_date
        return result
