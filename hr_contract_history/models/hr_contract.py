# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class HrContract(models.Model):
    _inherit = 'hr.contract'

    historicals = fields.One2many(
        comodel_name='hr.contract.historical', inverse_name='contract',
        string='Contract history')


class HrContractHistorical(models.Model):
    _name = 'hr.contract.historical'
    _description = 'Historical of contract'

    contract = fields.Many2one(
        'hr.contract', string='Contract')
    type = fields.Selection([('new', 'New'),
                             ('mod', 'Modification'),
                             ('end', 'end')], string="Type")
    date = fields.Date('date')
    description = fields.Char('Description')
