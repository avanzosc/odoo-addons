# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone, utc


class WizEventAppendAssistant(models.TransientModel):
    _name = 'wiz.event.append.assistant'

    from_date = fields.Date(string='From date')
    to_date = fields.Date(string='To date')
    partner = fields.Many2one('res.partner', string='Partner')
    min_event = fields.Many2one('event.event', string='Min. event')
    min_from_date = fields.Date(string='Min. from date')
    max_event = fields.Many2one('event.event', string='Max. event')
    max_to_date = fields.Date(string='Max. to date')

    @api.model
    def default_get(self, var_fields):
        event_obj = self.env['event.event']
        res = super(WizEventAppendAssistant, self).default_get(var_fields)
        from_date = False
        to_date = False
        for event in event_obj.browse(self.env.context.get('active_ids')):
            if not from_date or event.date_begin < from_date:
                new_date = self._convert_date_to_local_format_with_hour(
                    event.date_begin).date()
                res.update({'from_date': new_date.strftime('%Y-%m-%d'),
                            'min_from_date': new_date.strftime('%Y-%m-%d'),
                            'min_event': event.id})
                from_date = self._prepare_date_for_control(new_date)
            if not to_date or event.date_end > to_date:
                new_date = self._convert_date_to_local_format_with_hour(
                    event.date_end).date()
                res.update({'to_date': new_date.strftime('%Y-%m-%d'),
                            'max_to_date': new_date.strftime('%Y-%m-%d'),
                            'max_event': event.id})
                to_date = self._prepare_date_for_control(new_date)
        return res

    @api.multi
    @api.onchange('from_date', 'to_date')
    def onchange_dates(self):
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
            if self.from_date > self.max_to_date:
                self.from_date = self.min_from_date
                self.to_date = self.max_to_date
                return {'warning': {
                        'title': _('Error in from date'),
                        'message':
                        (_('From date greater than end date of the event %s') %
                         self.max_event.name)}}
        if self.to_date:
            if self.to_date < self.min_from_date:
                self.from_date = self.min_from_date
                self.to_date = self.max_to_date
                return {'warning': {
                        'title': _('Error in to date'),
                        'message':
                        (_('to date less than start date of the event %s') %
                         self.min_event.name)}}
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
        new_date = self._put_utc_format_date(date, 0.0).strftime(
            "%Y-%m-%d %H:%M:%S")
        return new_date

    @api.multi
    def action_append(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        registration_obj = self.env['event.registration']
        track_obj = self.env['event.track']
        for event in event_obj.browse(self.env.context.get('active_ids')):
            registration = event.registration_ids.filtered(
                lambda x: x.partner_id.id == self.partner.id)
            if registration:
                if not registration.date_start:
                    self._update_registration_start_date(registration)
                if not registration.date_end:
                    self._update_registration_date_end(registration)
                registration.state = 'open'
            else:
                vals = self._prepare_registration_data(event)
                contact_id = self.partner.address_get().get('default', False)
                if contact_id:
                    contact = self.env['res.partner'].browse(contact_id)
                    vals.update({'name': contact.name,
                                 'email': contact.email,
                                 'phone': contact.phone})
                registration = registration_obj.create(vals)
            registration.confirm_registration()
            registration.mail_user()
            cond = self._prepare_track_condition_search(event)
            tracks = track_obj.search(cond)
            for track in tracks:
                presence = track.presences.filtered(
                    lambda x: x.session == track and x.event == event and
                    x.partner == self.partner)
                if presence:
                    self._put_pending_presence_state(presence)
                else:
                    self._create_presence_from_wizard(track, event)
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

    def _put_pending_presence_state(self, presence):
        presence.state = 'pending'

    def _prepare_track_condition_search(self, event):
        from_date, to_date = self._calc_dates_for_search_track(
            self.from_date, self.to_date)
        cond = [('id', 'in', event.track_ids.ids),
                ('date', '!=', False),
                ('date', '>=', from_date),
                ('date', '<=', to_date)]
        return cond

    def _update_registration_start_date(self, registration):
        from_date = self._convert_date_to_local_format(self.from_date).date()
        registration.date_start = self._put_utc_format_date(from_date, 0.0)

    def _update_registration_date_end(self, registration):
        to_date = self._convert_date_to_local_format(self.to_date).date()
        registration.date_end = self._put_utc_format_date(to_date, 0.0)

    def _prepare_registration_data(self, event):
        vals = {'event_id': event.id,
                'partner_id': self.partner.id,
                'state': 'open',
                'date_start': self._put_utc_format_date(
                    self.from_date, 0.0),
                'date_end': self._put_utc_format_date(
                    self.to_date, 0.0)}
        return vals

    def _calc_dates_for_search_track(self, from_date, to_date):
        from_date = self._put_utc_format_date(
            from_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        to_date = self._put_utc_format_date(
            to_date, 0.0).strftime('%Y-%m-%d %H:%M:%S')
        return from_date, to_date

    def _put_utc_format_date(self, date, time):
        new_date = (datetime.strptime(str(date), '%Y-%m-%d') +
                    relativedelta(hours=float(time)))
        local = timezone(self.env.user.tz)
        local_dt = local.localize(new_date, is_dst=None)
        utc_dt = local_dt.astimezone(utc)
        return utc_dt

    def _convert_date_to_local_format(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date

    def _convert_date_to_local_format_with_hour(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date

    def _create_presence_from_wizard(self, track, event):
        presence_obj = self.env['event.track.presence']
        vals = {'session': track.id,
                'event': event.id,
                'partner': self.partner.id}
        presence = presence_obj.create(vals)
        return presence
