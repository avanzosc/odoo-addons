# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    def _add_follower(self, partner):
        follower_obj = self.env['mail.followers']
        if partner.id not in self.message_follower_ids.ids:
            follower_obj.create({'res_model': 'event.event',
                                 'res_id': self.id,
                                 'partner_id': partner.id})


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.model
    def create(self, values):
        registration = super(EventRegistration, self).create(values)
        if values.get('partner_id', False) and registration.event_id:
            registration.event_id._add_follower(registration.partner_id)
        return registration

    @api.multi
    def write(self, values):
        res = super(EventRegistration, self).write(values)
        if values.get('partner_id', False):
            for registration in self:
                if registration.event_id:
                    registration.event_id._add_follower(
                        registration.partner_id)
        return res
