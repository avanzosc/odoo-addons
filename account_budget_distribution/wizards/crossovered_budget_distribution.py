# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrossoveredBudgetDistribution(models.TransientModel):
    _name = 'crossovered.budget.distribution'
    _description = 'Budget Distribution Wizard'

    budget_id = fields.Many2one(comodel_name='crossovered.budget')
    line_ids = fields.One2many(
        comodel_name='crossovered.budget.distribution.line',
        inverse_name='distribution_id')

    @api.model
    def default_get(self, fields):
        context = self.env.context
        res = super(CrossoveredBudgetDistribution, self).default_get(fields)
        if context.get('active_model') == 'crossovered.budget':
            budget = self.env[context.get('active_model')].browse(
                context.get('active_id'))
            res.update({
                'budget_id': budget.id,
                'line_ids': [
                    (0, 0, {'budget_post_id': x.general_budget_id.id,
                            'planned_amount': x.planned_amount})
                    for x in budget.summary_ids],
            })
        return res

    @api.multi
    def button_distribute_amount(self):
        for wiz in self:
            for line in wiz.line_ids:
                budget_lines = wiz.budget_id.crossovered_budget_line.filtered(
                    lambda l: l.general_budget_id == line.budget_post_id)
                try:
                    budget_lines = budget_lines.filtered(
                        lambda l: not l.general_budget_id.expenses)
                except Exception:
                    pass
                if budget_lines:
                    budget_lines.write({
                        'planned_amount': (
                            line.planned_amount / len(budget_lines))
                    })


class CrossoveredBudgetDistributionLine(models.TransientModel):
    _name = 'crossovered.budget.distribution.line'
    _description = 'Budget Distribution Line'

    distribution_id = fields.Many2one(
        comodel_name='crossovered.budget.distribution')
    budget_post_id = fields.Many2one(
        comodel_name='account.budget.post')
    planned_amount = fields.Float()
