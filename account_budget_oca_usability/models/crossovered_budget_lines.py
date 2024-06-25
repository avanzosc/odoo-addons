# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    practical_amount = fields.Float(store=True, copy=False)
    difference = fields.Float(
        string="Difference",
        store=True,
        copy=False,
        digits=0,
        compute="_compute_difference",
    )

    @api.depends(
        "general_budget_id",
        "general_budget_id.account_ids",
        "date_from",
        "date_to",
        "analytic_account_id",
        "analytic_account_id.line_ids",
        "analytic_account_id.line_ids.date",
        "analytic_account_id.line_ids.general_account_id",
    )
    def _compute_practical_amount(self):
        result = super()._compute_practical_amount()
        return result

    @api.depends("planned_amount", "practical_amount")
    def _compute_difference(self):
        for line in self:
            difference = 0
            if line.practical_amount:
                difference = line.practical_amount - line.planned_amount
            line.difference = difference
