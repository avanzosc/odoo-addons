# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    communication_seg_soc_code = fields.Char('Seg. Soc. communication code')
    communication_contract_code = fields.Char('Contract communication code')
    historicals = fields.One2many(
        comodel_name='hr.contract.historical', inverse_name='contract',
        string='Contract history')


class HrContractHistorical(models.Model):
    _name = 'hr.contract.historical'
    _description = 'Historical of contract'

    @api.depends('hours')
    def _calculate_hours_percentage(self):
        for history in self:
            history.percentage = 0
            weekly_hours = history.contract.employee_id.company_id.weekly_hours
            if history.hours > 0 and weekly_hours:
                history.percentage = (history.hours * 100) / weekly_hours

    contract = fields.Many2one(
        'hr.contract', string='Contract')
    type = fields.Selection([('new', 'New'),
                             ('mod', 'Modification'),
                             ('end', 'end')], string="Type")
    date = fields.Date('date')
    hours = fields.Float(string='Hours')
    percentage = fields.Float(
        string='Percentage', digits=(2, 2), store=True,
        compute='_calculate_hours_percentage')
    description = fields.Char('Description')
