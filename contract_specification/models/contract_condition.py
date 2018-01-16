# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class ContractCondition(models.Model):
    _name = 'contract.condition'
    _description = 'Contract Condition'
    _inherit = ['mail.thread']

    name = fields.Char(string='Title', translate=True, required=True)
    description = fields.Text(string='Description', translate=True)
    template_ids = fields.Many2many(
        comodel_name='contract.condition.template', string='Templates',
        relation='rel_condition_template', column1='condition_id',
        column2='template_id')
