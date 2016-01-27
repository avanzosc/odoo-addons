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
        for event in event_obj.browse(self.env.context.get('active_ids')):
            registrations = event.registration_ids.filtered(
                lambda x: x.partner_id.id == self.partner.id)
            if registrations:
                registration = registrations[0]
            else:
                vals = {'event_id': event.id,
                        'partner_id': self.partner.id}
                contact_id = self.partner.address_get().get('default', False)
                if contact_id:
                    contact = self.env['res.partner'].browse(contact_id)
                    vals.update({'name': contact.name,
                                 'email': contact.email,
                                 'phone': contact.phone})
                registration = registration_obj.create(vals)
            cond = [('id', 'in', event.track_ids.ids),
                    '|', ('date', '=', False), '&',
                    ('date', '>=', self.from_date),
                    ('date', '<=', self.to_date)]
            tracks = track_obj.search(cond)
            for track in tracks:
                if registration.id not in track.registrations.ids:
                    track.registrations = [(4, registration.id)]
        return {'type': 'ir.actions.act_window_close'}
