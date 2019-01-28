# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    summary_ids = fields.One2many(
        comodel_name='crossovered.budget.summary',
        inverse_name='crossovered_budget_id', string='Summary Lines')
