# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class WizEventDeleteAssistant(models.TransientModel):
    _name = 'wiz.event.delete.assistant'

    from_date = fields.Date(string='From date', required=True)
    to_date = fields.Date(string='To date', required=True)
    partner = fields.Many2one(
        'res.partner', string='Partner', required=True)
    past_sessions = fields.Boolean('Past Sessions')
    later_sessions = fields.Boolean('Later Sessions')
    message = fields.Char('Message', readonly=True)

    @api.onchange('from_date', 'to_date', 'partner')
    def onchange_information(self):
        event_track_obj = self.env['event.track']
        self.past_sessions = False
        self.later_sessions = False
        self.message = ''
        if self.from_date and self.to_date and self.partner:
            sessions = self.partner.sessions.filtered(
                lambda x: x.event_id.id in self.env.context.get('active_ids'))
            cond = [('id', 'in', sessions.ids),
                    ('date', '<', self.from_date)]
            prev = event_track_obj.search(cond, limit=1)
            if prev:
                self.past_sessions = True
            cond = [('id', 'in', sessions.ids),
                    ('date', '>', self.to_date)]
            later = event_track_obj.search(cond, limit=1)
            if later:
                self.later_sessions = True
            if self.past_sessions and self.later_sessions:
                self.message = _('This person has sessions with dates before'
                                 ' and after')
            elif self.past_sessions:
                self.message = _('This person has sessions with dates before')
            elif self.later_sessions:
                self.message = _('This person has sessions with dates after')

    @api.multi
    def action_delete(self):
        self.ensure_one()
        registration_obj = self.env['event.registration']
        cond = [('event_id', 'in', self.env.context.get('active_ids')),
                ('partner_id', '=', self.partner.id)]
        registrations = registration_obj.search(cond)
        registrations.unlink()
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def action_delete_past_and_later(self):
        self.ensure_one()
        self.action_delete()

    @api.multi
    def action_nodelete_past_and_later(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        event_track_obj = self.env['event.track']
        registration_obj = self.env['event.registration']
        for event in event_obj.browse(self.env.context.get('active_ids')):
            sessions = self.partner.sessions.filtered(
                lambda x: x.event_id.id == event.id)
            cond = [('id', 'in', sessions.ids),
                    ('date', '<', self.from_date)]
            prev = event_track_obj.search(cond, limit=1)
            cond = [('id', 'in', sessions.ids),
                    ('date', '>', self.to_date)]
            later = event_track_obj.search(cond, limit=1)
            if not prev and not later:
                cond = [('event_id', '=', event.id),
                        ('partner_id', '=', self.partner.id)]
                registrations = registration_obj.search(cond)
                registrations.unlink()
            else:
                self._delete_registrations_between_dates(sessions)
        return {'type': 'ir.actions.act_window_close'}

    def _delete_registrations_between_dates(self, sessions):
        event_track_obj = self.env['event.track']
        cond = [('id', 'in', sessions.ids),
                '|', ('date', '=', False), '&',
                ('date', '>=', self.from_date),
                ('date', '<=', self.to_date)]
        tracks = event_track_obj.search(cond)
        for track in tracks:
            for regis in track.registrations:
                if regis.partner_id.id == self.partner.id:
                    track.registrations = [(3, regis.id)]
