# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    history_ids = fields.One2many(
        comodel_name='hr.contract.history', inverse_name='contract_id',
        string='Contract history')


class HrContractHistorical(models.Model):
    _name = 'hr.contract.history'
    _description = 'Historical of contract'

    contract_id = fields.Many2one(
        comodel_name='hr.contract', string='Contract')
    type = fields.Selection(
        selection=[('new', 'New'), ('mod', 'Modification'), ('end', 'end')],
        string="Type")
    date = fields.Date(string='date')
    description = fields.Char(string='Description')
