# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class WizEventDeleteAssistant(models.TransientModel):
    _inherit = 'wiz.event.delete.assistant'

    address_home_id = fields.Many2one(
        'res.partner', related='partner.employee.address_home_id',
        string='Employee')

    def _cancel_registration(self):
        registrations = super(WizEventDeleteAssistant,
                              self)._cancel_registration()
        registrations.write({'contract': False})
        return registrations

    def _cancel_presences(self):
        presences = super(WizEventDeleteAssistant, self)._cancel_presences()
        if self.address_home_id:
            for presence in presences:
                presence._update_employee_days(cancel_presence=True)
        return presences
