# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    history_ids = fields.One2many(
        comodel_name='hr.contract.history', inverse_name='contract_id',
        string='Contract history')


class HrContractHistorical(models.Model):
    _name = 'hr.contract.history'
    _description = 'History of contract'

    @api.depends('hours')
    def _compute_hours_percentage(self):
        for history in self:
            percentage = 0
            weekly_hours =\
                history.contract_id.employee_id.company_id.weekly_hours
            if history.hours > 0 and weekly_hours:
                percentage = (history.hours * 100) / weekly_hours
            history.percentage = percentage

    contract_id = fields.Many2one(
        comodel_name='hr.contract', string='Contract')
    type = fields.Selection(
        selection=[('new', 'New'), ('mod', 'Modification'), ('end', 'End')],
        string="Type")
    date = fields.Date(string='Date')
    hours = fields.Float(string='Hours')
    percentage = fields.Float(
        string='Percentage', digits=(2, 2), store=True,
        compute='_compute_hours_percentage')
    communication_soc_seg_code = fields.Char(
        string='Soc. Seg. Communication Code')
    communication_contract_code = fields.Char(
        string='Contract Communication Code')
    description = fields.Char(string='Description')
