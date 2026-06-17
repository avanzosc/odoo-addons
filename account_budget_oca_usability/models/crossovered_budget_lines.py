# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    result_amount = fields.Float()
    practical_amount = fields.Float(
        store=True,
    )
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

    @api.depends("planned_amount", "practical_amount")
    def _compute_difference(self):
        for line in self:
            difference = 0
            if line.practical_amount:
                difference = line.practical_amount - line.planned_amount
            line.difference = difference

    def button_recompute_practical_amount(self):
        fnames = ["practical_amount"]
        for fname in fnames:
            self.env.add_to_compute(self._fields[fname], self)
        self.modified(fnames)

    def action_recalculate_result_amount(self):
        for line in self:
            line.result_amount = line.practical_amount - line.planned_amount

    def _cron_recompute_practical_amount(self):
        recompute_lines = self.search(
            [
                ("crossovered_budget_id.state", "!=", "cancel"),
            ]
        )
        recompute_lines.button_recompute_practical_amount()
