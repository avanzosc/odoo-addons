# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    related_taxes_amount = fields.Float(
        compute="_compute_related_taxes_amount",
    )

    @api.depends("account_id")
    def _compute_related_taxes_amount(self):
        for line in self:
            amount = 0
            if line.account_id:
                now_year = fields.Datetime.now().year
                lines = (
                    self.env["account.move.line"]
                    .search(
                        [
                            ("account_id", "=", line.account_id.id),
                            ("parent_state", "=", "posted"),
                        ]
                    )
                    .filtered(lambda c: c.date.year == now_year)
                )
                if lines:
                    amount = sum(lines.mapped("balance"))
            line.related_taxes_amount = amount
