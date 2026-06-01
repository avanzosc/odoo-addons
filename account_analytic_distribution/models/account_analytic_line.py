# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    account_move_id = fields.Many2one(
        string="Journal Entry",
        comodel_name="account.move",
        related="move_line_id.move_id",
        store=True,
        readonly=True,
    )
    pre_amount = fields.Float(string="Input Amount")

    @api.onchange("pre_amount")
    def onchange_pre_amount(self):
        self.amount = abs(self.pre_amount)
        if self.move_line_id and self.move_line_id.debit != 0:
            self.amount = -1 * abs(self.pre_amount)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name") == "/ -- /" and vals.get("move_line_id"):
                vals["name"] = (
                    self.env["account.move.line"]
                    .browse(vals.get("move_line_id"))
                    .account_id.display_name
                )
            if "amount" in vals:
                vals["pre_amount"] = abs(vals["amount"])
        return super().create(vals_list)
