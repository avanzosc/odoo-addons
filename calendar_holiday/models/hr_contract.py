# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class HrContract(models.Model):
    _name = 'hr.contract'
    _inherit = ['hr.contract', 'mail.thread', 'ir.needaction_mixin']

    holiday_calendars = fields.Many2many(
        comodel_name='calendar.holiday', string='Holiday calendars')
    partner = fields.Many2one(
        comodel_name='res.partner', string='Contract employee',
        related='employee_id.address_home_id')
    calendar_days = fields.One2many(
        comodel_name='res.partner.calendar.day', inverse_name='contract',
        string='Employee calendar days')

    @api.model
    def create(self, vals):
        follower_obj = self.env['mail.followers']
        contract = super(HrContract, self).create(vals)
        if (contract.partner and contract.partner.id not in
                contract.message_follower_ids.ids):
            follower_obj.create({'res_model': 'hr.contract',
                                 'res_id': contract.id,
                                 'partner_id': contract.partner.id})
        return contract

    @api.multi
    def write(self, vals):
        follower_obj = self.env['mail.followers']
        result = super(HrContract, self).write(vals)
        if vals.get('partner', False):
            for contract in self:
                if (vals.get('partner') not in
                        contract.message_follower_ids.ids):
                    follower_obj.create({'res_model': 'hr.contract',
                                         'res_id': contract.id,
                                         'partner_id': vals.get('partner')})
        return result
