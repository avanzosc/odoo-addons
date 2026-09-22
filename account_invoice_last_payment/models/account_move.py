# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    last_payment_date = fields.Date(
        compute="_compute_last_payment_date",
        store=True,
    )

    @api.depends("line_ids", "payment_state")
    def _compute_last_payment_date(self):
        for move in self:
            if not move.is_invoice():
                move.last_payment_date = False
                continue
            reconciled_partials = move.sudo()._get_all_reconciled_invoice_partials()
            dates = []
            for reconciled_partial in reconciled_partials:
                counterpart_line = reconciled_partial["aml"]
                if counterpart_line.date:
                    dates.append(counterpart_line.date)
            move.last_payment_date = max(dates) if dates else False
