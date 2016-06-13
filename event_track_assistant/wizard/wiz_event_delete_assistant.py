# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class WizEventDeleteAssistant(models.TransientModel):
    _name = 'wiz.event.delete.assistant'

    from_date = fields.Date(string='From date')
    to_date = fields.Date(string='To date')
    registration = fields.Many2one(
        'event.registration', string='Partner registration')
    partner = fields.Many2one('res.partner', string='Partner')
    min_event = fields.Many2one('event.event', string='Min. event')
    min_from_date = fields.Date(string='Min. from date')
    max_event = fields.Many2one('event.event', string='Max. event')
    max_to_date = fields.Date(string='Max. to date')
    past_sessions = fields.Boolean('Past Sessions')
    later_sessions = fields.Boolean('Later Sessions')
    message = fields.Char('Message', readonly=True)

    @api.model
    def default_get(self, var_fields):
        event_obj = self.env['event.event']
        res = super(WizEventDeleteAssistant, self).default_get(var_fields)
        from_date = False
        to_date = False
        for event in event_obj.browse(self.env.context.get('active_ids')):
            if not from_date or event.date_begin < from_date:
                new_date = event_obj._convert_date_to_local_format_with_hour(
                    event.date_begin).date()
                res.update({'from_date': new_date.strftime('%Y-%m-%d'),
                            'min_from_date': new_date.strftime('%Y-%m-%d'),
                            'min_event': event.id})
                from_date = self._prepare_date_for_control(new_date)
            if not to_date or event.date_end > to_date:
                new_date = event_obj._convert_date_to_local_format_with_hour(
                    event.date_end).date()
                res.update({'to_date': new_date.strftime('%Y-%m-%d'),
                            'max_to_date': new_date.strftime('%Y-%m-%d'),
                            'max_event': event.id})
                to_date = self._prepare_date_for_control(new_date)
        return res

    @api.onchange('from_date', 'to_date', 'partner')
    def onchange_information(self):
        event_obj = self.env['event.event']
        event_track_obj = self.env['event.track']
        self.past_sessions = False
        self.later_sessions = False
        self.message = ''
        if self.from_date and self.to_date and self.partner:
            if self.registration:
                sessions = self.partner.sessions.filtered(
                    lambda x: x.event_id.id == self.registration.event_id.id)
                from_date = event_obj._put_utc_format_date(
                    self.from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
                to_date = event_obj._put_utc_format_date(
                    self.to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
                if self.registration.date_start != from_date:
                    self.past_sessions = True
                if self.registration.date_end != to_date:
                    self.later_sessions = True
            else:
                sessions = self.partner.sessions.filtered(
                    lambda x: x.event_id.id in
                    self.env.context.get('active_ids'))
                cond = self._prepare_track_condition_from_date(sessions)
                prev = event_track_obj.search(cond, limit=1)
                if prev:
                    self.past_sessions = True
                cond = self._prepare_track_condition_to_date(sessions)
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
    @api.onchange('from_date', 'to_date')
    def _dates_control(self):
        self.ensure_one()
        res = {}
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                self.from_date = self.min_from_date
                self.to_date = self.max_to_date
                return {'warning': {
                        'title': _('Error in from date'),
                        'message':
                        (_('From date greater than date to'))}}
        if self.from_date:
            if self.from_date < self.min_from_date:
                self.from_date = self.min_from_date
                self.to_date = self.max_to_date
                return {'warning': {
                        'title': _('Error in from date'),
                        'message':
                        (_('From date less than start date of the event %s') %
                         self.min_event.name)}}
        if self.to_date:
            if self.to_date > self.max_to_date:
                self.from_date = self.min_from_date
                self.to_date = self.max_to_date
                return {'warning': {
                        'title': _('Error in to date'),
                        'message':
                        (_('From date greater than end date of the event %s') %
                         self.max_event.name)}}
        return res

    def _prepare_date_for_control(self, date):
        event_obj = self.env['event.event']
        new_date = event_obj._put_utc_format_date(date, 0.0).strftime(
            "%Y-%m-%d %H:%M:%S")
        return new_date

    def _prepare_track_condition_from_date(self, sessions):
        event_obj = self.env['event.event']
        from_date = event_obj._put_utc_format_date(
            self.from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '!=', False),
                ('date', '<', from_date)]
        return cond

    def _prepare_track_condition_to_date(self, sessions):
        event_obj = self.env['event.event']
        to_date = event_obj._put_utc_format_date(
            self.to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '!=', False),
                ('date', '>', to_date)]
        return cond

    @api.multi
    def action_delete(self):
        self.ensure_one()
        self._cancel_registration()
        self._cancel_presences()
        return self._open_event_tree_form()

    @api.multi
    def action_delete_past_and_later(self):
        self.ensure_one()
        self.action_delete()

    @api.multi
    def action_nodelete_past_and_later(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        presence_obj = self.env['event.track.presence']
        if self.registration:
            events = [self.registration.event_id]
        else:
            events = event_obj.browse(self.env.context.get('active_ids'))
        for event in events:
            sessions = self.partner.sessions.filtered(
                lambda x: x.event_id == event)
            self._delete_registrations_between_dates(sessions)
            if self.registration:
                registrations = [self.registration]
            else:
                registrations = event.registration_ids.filtered(
                    lambda x: x.partner_id == self.partner and
                    x.state == 'open')
            from_date, to_date = self._prepare_dates_for_search_registrations()
            for registration in registrations:
                cond = [('event', '=', event.id),
                        ('partner', '=', self.partner.id),
                        ('state', '!=', 'cancel'),
                        ('session_date', '>=', registration.date_start),
                        ('session_date', '<=', registration.date_end), '|',
                        ('session_date', '<', from_date),
                        ('session_date', '>', to_date)]
                presences = presence_obj.search(cond, limit=1)
                if not presences:
                    registration.state = 'cancel'
        return self._open_event_tree_form()

    def _prepare_dates_for_search_registrations(self):
        event_obj = self.env['event.event']
        from_date = event_obj._put_utc_format_date(
            self.from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        to_date = event_obj._put_utc_format_date(
            self.to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        return from_date, to_date

    def _cancel_registration(self):
        if self.registration:
            registrations = self.registration
        else:
            cond = [('event_id', 'in', self.env.context.get('active_ids')),
                    ('partner_id', '=', self.partner.id),
                    ('state', '=', 'open')]
            registrations = self.env['event.registration'].search(cond)
        registrations.write({'state': 'cancel'})
        return registrations

    def _cancel_presences(self):
        if self.registration:
            cond = [('event', '=', self.registration.event_id.id),
                    ('session_date', '>=', self.registration.date_start),
                    ('session_date', '<=', self.registration.date_end)]
        else:
            cond = [('event', 'in', self.env.context.get('active_ids'))]
        cond.append(('partner', '=', self.partner.id))
        presences = self.env['event.track.presence'].search(cond)
        presences.write({'state': 'canceled'})
        return presences

    def _delete_registrations_between_dates(self, sessions):
        event_track_obj = self.env['event.track']
        cond = self._prepare_track_search_condition_for_delete(sessions)
        tracks = event_track_obj.search(cond)
        for track in tracks:
            presence = track.presences.filtered(
                lambda x: x.partner == self.partner)
            if presence:
                presence.state = 'canceled'

    def _prepare_track_search_condition_for_delete(self, sessions):
        event_obj = self.env['event.event']
        from_date = event_obj._put_utc_format_date(
            self.from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        to_date = event_obj._put_utc_format_date(
            self.to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '!=', False),
                ('date', '>=', from_date),
                ('date', '<=', to_date)]
        return cond

    def _open_event_tree_form(self):
        result = {'name': _('Event'),
                  'type': 'ir.actions.act_window',
                  'res_model': 'event.event',
                  'view_type': 'form',
                  'view_mode': 'form,kanban,calendar,tree',
                  'res_id': self.env.context.get('active_ids')[0],
                  'target': 'current',
                  'context': self.env.context}
        if len(self.env.context.get('active_ids')) > 1:
            result['view_mode'] = 'kanban,calendar,tree,form'
        return result
