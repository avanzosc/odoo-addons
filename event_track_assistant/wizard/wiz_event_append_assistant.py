# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizEventAppendAssistant(models.TransientModel):
    _name = 'wiz.event.append.assistant'

    from_date = fields.Date(string='From date', required=True)
    to_date = fields.Date(string='To date', required=True)
    partner = fields.Many2one(
        'res.partner', string='Partner', required=True)

    @api.multi
    def action_append(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        registration_obj = self.env['event.registration']
        track_obj = self.env['event.track']
        presence_obj = self.env['event.track.presence']
        for event in event_obj.browse(self.env.context.get('active_ids')):
            registration = event.registration_ids.filtered(
                lambda x: x.partner_id.id == self.partner.id)
            if registration:
                if not registration.date_start:
                    registration.date_start = self.from_date
                if not registration.date_end:
                    registration.date_end = self.to_date
                registration.state = 'open'
            else:
                vals = {'event_id': event.id,
                        'partner_id': self.partner.id,
                        'state': 'open',
                        'date_start': self.from_date,
                        'date_end': self.to_date}
                contact_id = self.partner.address_get().get('default', False)
                if contact_id:
                    contact = self.env['res.partner'].browse(contact_id)
                    vals.update({'name': contact.name,
                                 'email': contact.email,
                                 'phone': contact.phone})
                registration_obj.create(vals)
            cond = [('id', 'in', event.track_ids.ids),
                    '|', ('date', '=', False), '&',
                    ('date', '>=', self.from_date),
                    ('date', '<=', self.to_date)]
            tracks = track_obj.search(cond)
            for track in tracks:
                presence = track.presences.filtered(
                    lambda x: x.session == track and x.event == event and
                    x.partner == self.partner)
                if presence:
                    presence.state = 'pending'
                else:
                    vals = {'session': track.id,
                            'event': event.id,
                            'partner': self.partner.id}
                    presence_obj.create(vals)
        return {'type': 'ir.actions.act_window_close'}
