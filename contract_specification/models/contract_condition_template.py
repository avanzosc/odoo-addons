# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class ContractConditionTemplate(models.Model):
    _name = 'contract.condition.template'
    _description = 'Contract Conditions Template'
    _inherit = ['mail.thread']

    name = fields.Char(string='Title', translate=True, required=True)
    condition_ids = fields.Many2many(
        comodel_name='contract.condition', string='Conditions',
        relation='rel_condition_template', column1='template_id',
        column2='condition_id')
