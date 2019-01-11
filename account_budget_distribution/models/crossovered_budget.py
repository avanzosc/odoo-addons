# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    total_planned_amount = fields.Float(
        string='Total Planned Amount', store=True)
    summary_ids = fields.One2many(
        comodel_name='crossovered.budget.summary',
        inverse_name='crossovered_budget_id', string='Summary Lines')

    @api.multi
    def button_divide_planned_amount(self):
        for budget in self.filtered('crossovered_budget_line'):
            try:
                budget_lines = budget.crossovered_budget_line.filtered(
                    lambda l: not l.general_budget_id.expenses)
            except Exception:
                budget_lines = budget.crossovered_budget_line
            budget_lines.write({
                'planned_amount': (
                        budget.total_planned_amount / len(budget_lines))
            })
