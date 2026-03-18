# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    result_amount = fields.Float()
    practical_amount = fields.Float(store=True)
    difference = fields.Float(
        store=True,
        copy=False,
        digits=0,
        compute="_compute_difference",
    )
    amount_type = fields.Selection(
        selection=[
            ("cost", "Cost"),
            ("revenue", "Revenue"),
        ],
        compute="_compute_amount_type",
        string="Cost/Revenue",
        store=True,
    )

    @api.depends("planned_amount")
    def _compute_amount_type(self):
        for line in self:
            line.amount_type = "cost" if line.planned_amount <= 0 else "revenue"

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

    def action_recalculate_result_amount(self):
        for line in self:
            line.result_amount = line.practical_amount - line.planned_amount
