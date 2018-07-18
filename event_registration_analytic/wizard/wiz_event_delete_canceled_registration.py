# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizEventDeleteCanceledRegistration(models.TransientModel):
    _name = 'wiz.event.delete.canceled.registration'

    @api.multi
    def delete_canceled_registration(self):
        event_obj = self.env['event.event']
        for event in event_obj.browse(self.env.context.get('active_ids')):
            event._delete_canceled_presences_registrations()
