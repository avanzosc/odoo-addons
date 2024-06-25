# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    pre_amount = fields.Float(string="Amount")

    @api.onchange("pre_amount")
    def onchange_pre_amount(self):
        self.amount = abs(self.pre_amount)
        if self.move_id.debit != 0:
            self.amount = (-1) * abs(self.pre_amount)

    @api.model
    def create(self, values):
        if "name" in values and values["name"] == "/ -- /" and "move_id" in values:
            values["name"] = (
                self.env["account.move.line"]
                .browse(values.get("move_id"))
                .account_id.display_name
            )
        if "amount" in values:
            values["pre_amount"] = values["amount"]
        return super().create(values)
