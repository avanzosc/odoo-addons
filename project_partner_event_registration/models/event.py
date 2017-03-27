# -*- coding: utf-8 -*-
# (c) 2016 Oihane Crucelaegui - AvanzOSC
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.one
    def assign_partners(self):
        registry_obj = self.env['event.registration']
        for partner in self.project_id.partners:
            if not registry_obj.search_count(
                    [('event_id', '=', self.id),
                     ('partner_id', '=', partner.id)]):
                registry_obj.create({
                    'partner_id': partner.id,
                    'event_id': self.id,
                    'name': partner.name,
                    'email': partner.email,
                    'phone': partner.phone,
                    'message_follower_ids': [
                        (4, partner.id),
                        (4, self.user_id.partner_id.id)]})
