# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        if vals.get('project_id', False):
            event._add_followers_from_event_project()
        return event

    @api.multi
    def write(self, vals):
        super(EventEvent, self).write(vals)
        if vals.get('project_id', False):
            self._add_followers_from_event_project()
        return True

    def _add_followers_from_event_project(self):
        follower_obj = self.env['mail.followers']
        for event in self:
            for partner in (event.project_id.members.mapped(
                'partner_id').filtered(lambda x: x not in
                                       event.message_follower_ids) |
                event.project_id.mapped('message_follower_ids').filtered(
                    lambda x: x not in event.message_follower_ids)):
                follower_obj.create({'res_model': 'event.event',
                                     'res_id': event.id,
                                     'partner_id': partner.id})
