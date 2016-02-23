# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone, utc


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
                    presence.state = 'pending'
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
            result['view_mode'] = 'kanban,calendar,tree, form'
        return result

    def _prepare_track_condition_search(self, event):
        from_date, to_date = self._calc_dates_for_search_track(
            self.from_date, self.to_date)
        cond = [('id', 'in', event.track_ids.ids),
                '|', ('date', '=', False), '&',
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

    def _create_presence_from_wizard(self, track, event):
        presence_obj = self.env['event.track.presence']
        vals = {'session': track.id,
                'event': event.id,
                'partner': self.partner.id}
        presence_obj.create(vals)
