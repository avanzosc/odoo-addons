# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    result_amount = fields.Float(
        string="Result Amount",
    )

    def action_recalculate_result_amount(self):
        for line in self:
            line.result_amount = line.practical_amount - line.planned_amount

    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        result = super().read_group(
            domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
        )
        for line in result:
            if "__domain" in line:
                lines = self.search(line["__domain"])
                practical_amount = sum(lines.mapped("practical_amount"))
                theoretical_amount = sum(lines.mapped("theoretical_amount"))
                result_amount = sum(lines.mapped("result_amount"))
                line["practical_amount"] = practical_amount
                line["theoretical_amount"] = theoretical_amount
                line["result_amount"] = result_amount
            else:
                fields.remove("practical_amount")
                fields.remove("theoretical_amount")
                fields.remove("result_amount")
        return result
