# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class CrossoveredBudgetDistribution(models.TransientModel):
    _name = 'crossovered.budget.distribution'
    _description = 'Budget Distribution Wizard'

    budget_id = fields.Many2one(comodel_name='crossovered.budget')
    line_ids = fields.One2many(
        comodel_name='crossovered.budget.distribution.line')

    @api.model
    def default_get(self, fields):
        res = super(CrossoveredBudgetDistribution, self).default_get(fields)
        return res

    # @api.multi
    # def button_distribute_amount(self):
    #     for wiz in self:
    #         for budget_post in wiz.mapped('line_ids.budget_post_id'):



class CrossoveredBudgetDistributionLine(models.TransientModel):
    _name = 'crossovered.budget.distribution.line'
    _description = 'Budget Distribution Line'

    distribution_id = fields.Many2one(
        comodel_name='crossovered.budget.distribution')
    budget_post_id = fields.Many2one(
        comodel_name='account.budget.post')
    planned_amount = fields.Float()
