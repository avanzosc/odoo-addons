# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models
from odoo.addons.base.res.res_request import referenceable_models


@api.model
def template_type_selection(self):
    return [('quotation', 'Quotation'),
            ('order', 'Order'),
            ('both', 'Both')]


class ContractConditionTemplate(models.Model):
    _name = 'contract.condition.template'
    _description = 'Contract Conditions Template'
    _inherit = ['mail.thread']

    name = fields.Char(string='Title', translate=True, required=True)
    tmpl_model = fields.Selection(
        selection=referenceable_models, string='Applies to model')
    tmpl_type = fields.Selection(
        selection=template_type_selection, string='Type', default='both')
    condition_ids = fields.Many2many(
        comodel_name='contract.condition', string='Conditions',
        relation='rel_condition_template', column1='template_id',
        column2='condition_id')
