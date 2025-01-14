# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    last_payment_date = fields.Date(
        compute="_compute_last_payment_date",
        store=True,
    )

    @api.depends("line_ids")
    def _compute_last_payment_date(self):
        for move in self:
            if not move.is_invoice():
                move.last_payment_date = False
                continue
            reconciles = move._get_reconciled_info_JSON_values()
            reconciles_dates = [rec.get("date") for rec in reconciles]
            move.last_payment_date = (
                max(reconciles_dates) if reconciles_dates else False
            )
