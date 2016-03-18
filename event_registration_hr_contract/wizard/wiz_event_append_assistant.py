# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    contract = fields.Many2one('hr.contract', string='Employee contract')
    address_home_id = fields.Many2one(
        'res.partner', related='partner.employee.address_home_id',
        string='Employee')

    @api.multi
    @api.onchange('partner')
    def onchange_partner(self):
        self.ensure_one()
        contract_obj = self.env['hr.contract']
        res = {}
        if self.partner:
            cond = [('partner', '=', self.partner.id),
                    ('date_start', '<=', self.from_date)]
            contracts = contract_obj.search(cond)
            self.contract = contracts[0].id
        return res

    def _prepare_registration_data(self, event):
        vals = super(WizEventAppendAssistant,
                     self)._prepare_registration_data(event)
        if self.contract:
            vals['contract'] = self.contract.id
        return vals

    def _create_presence_from_wizard(self, track, event):
        presence = super(WizEventAppendAssistant,
                         self)._create_presence_from_wizard(track, event)
        presence.absence_type = track.absence_type
        if self.address_home_id:
            presence._update_employee_days()
        return presence

    def _put_pending_presence_state(self, presence):
        res = super(WizEventAppendAssistant,
                    self)._put_pending_presence_state(presence)
        if self.address_home_id:
            presence._update_employee_days()
        return res
