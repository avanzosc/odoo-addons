# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _
from datetime import datetime
from pytz import timezone, utc


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    min_from_date = fields.Datetime(string='Min. from date', required=True)
    max_to_date = fields.Datetime(string='Max. to date', required=True)
    start_time = fields.Float(string='Start time', default=0.0)
    end_time = fields.Float(string='End time', default=0.0)

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
                            'start_time':
                            self._convert_times_to_float(event.date_begin),
                            'min_from_date': event.date_begin,
                            'min_event': event.id})
                from_date = self._prepare_date_for_control(new_date)
            if not to_date or event.date_end > to_date:
                new_date = self._convert_date_to_local_format_with_hour(
                    event.date_end).date()
                res.update({'todate': new_date.strftime('%Y-%m-%d'),
                            'end_time':
                            self._convert_times_to_float(event.date_end),
                            'max_to_date': event.date_end,
                            'max_event': event.id})
                to_date = self._prepare_date_for_control(new_date)
        if res or (self.from_date and self.to_date):
            res = self._find_task_for_append_assistant(res)
        return res

    @api.multi
    @api.onchange('from_date', 'start_time', 'to_date', 'end_time')
    def onchange_dates(self):
        self.ensure_one()
        res = {}
        if self.from_date and self.to_date:
            from_date = self._put_utc_format_date(
                self.from_date, self.start_time).strftime("%Y-%m-%d %H:%M:%S")
            to_date = self._put_utc_format_date(
                self.to_date, self.end_time).strftime("%Y-%m-%d %H:%M:%S")
            if from_date > to_date:
                self._put_old_dates(self.min_from_date, self.max_to_date)
                return {'warning': {
                        'title': _('Error in from date'),
                        'message':
                        (_('From date greater than date to'))}}
        if self.from_date:
            from_date = self._put_utc_format_date(
                self.from_date, self.start_time).strftime("%Y-%m-%d %H:%M:%S")
            if from_date < self.min_from_date:
                self._put_old_dates(self.min_from_date, self.max_to_date)
                return {'warning': {
                        'title': _('Error in from date'),
                        'message':
                        (_('From date less than start date of the event %s') %
                         self.min_event.name)}}
            if from_date > self.max_to_date:
                self._put_old_dates(self.min_from_date, self.max_to_date)
                return {'warning': {
                        'title': _('Error in from date'),
                        'message':
                        (_('From date greater than end date of the event %s') %
                         self.max_event.name)}}
        if self.to_date:
            to_date = self._put_utc_format_date(
                self.to_date, self.end_time).strftime("%Y-%m-%d %H:%M:%S")
            if to_date < self.min_from_date:
                self._put_old_dates(self.min_from_date, self.max_to_date)
                return {'warning': {
                        'title': _('Error in to date'),
                        'message':
                        (_('to date less than start date of the event %s') %
                         self.min_event.name)}}
            if to_date > self.max_to_date:
                self._put_old_dates(self.min_from_date, self.max_to_date)
                return {'warning': {
                        'title': _('Error in to date'),
                        'message':
                        (_('From date greater than end date of the event %s') %
                         self.max_event.name)}}
        res = self._find_task_for_append_assistant(res)
        if not res:
            if not self.tasks:
                return {'warning': {
                        'title': _('Error in dates'),
                        'message':
                        _('Not tasks found for introduced dates')}}
        return res

    def _put_old_dates(self, min_from_date, max_to_date):
        self.from_date = self._convert_date_to_local_format(
            self.min_from_date).date()
        self.start_time = self._convert_times_to_float(self.min_from_date)
        self.to_date = self._convert_date_to_local_format(
            self.max_to_date).date()
        self.end_time = self._convert_times_to_float(self.max_to_date)

    def _prepare_tasks_search_condition(self, res):
        cond = []
        if res.get('from_date', self.from_date) and res.get('to_date',
                                                            self.to_date):
            from_date = self._convert_date_to_local_format(
                res.get('from_date', self.from_date)).date()
            from_date = self._put_utc_format_date(
                from_date, self.start_time).strftime('%Y-%m-%d %H:%M:%S')
            to_date = self._convert_date_to_local_format(
                res.get('to_date', self.to_date)).date()
            to_date = self._put_utc_format_date(
                to_date, self.end_time).strftime('%Y-%m-%d %H:%M:%S')
            cond = [('event_id', 'in', self.env.context.get('active_ids')),
                    ('date', '>=', from_date),
                    ('date', '<=', to_date)]
        return cond

    def _update_registration_start_date(self, registration):
        super(WizEventAppendAssistant, self)._update_registration_start_date(
            registration)
        from_date = self._convert_date_to_local_format(self.from_date).date()
        registration.date_start = self._put_utc_format_date(
            from_date, self.start_time)

    def _update_registration_date_end(self, registration):
        super(WizEventAppendAssistant, self)._update_registration_date_end(
            registration)
        to_date = self._convert_date_to_local_format(self.to_date).date()
        registration.date_end = self._put_utc_format_date(
            to_date, self.end_time)

    def _prepare_registration_data(self, event):
        date_start = self._convert_date_to_local_format(self.from_date).date()
        date_end = self._convert_date_to_local_format(self.to_date).date()
        vals = {'event_id': event.id,
                'partner_id': self.partner.id,
                'state': 'open',
                'date_start': self._put_utc_format_date(
                    date_start, self.start_time),
                'date_end': self._put_utc_format_date(
                    date_end, self.end_time)}
        return vals

    def _calc_dates_for_search_track(self, from_date, to_date):
        from_date = self._put_utc_format_date(
            from_date, self.start_time).strftime('%Y-%m-%d %H:%M:%S')
        to_date = self._put_utc_format_date(
            to_date, self.end_time).strftime('%Y-%m-%d %H:%M:%S')
        return from_date, to_date

    def _prepare_track_search_condition(self, event):
        cond = [('id', 'in', event.track_ids.ids),
                ('date', '=', False),
                ('date', '>=', self.from_date),
                ('date', '<=', self.to_date)]
        return cond

    def _convert_times_to_float(self, date):
        minutes = 0.0
        seconds = 0.0
        local_time = self._convert_date_to_local_format2(
            date).strftime("%H:%M:%S")
        time = local_time.split(':')
        hour = float(time[0])
        if int(time[1]) > 0:
            minutes = float(time[1]) / 60
        if int(time[2]) > 0:
            seconds = float(time[2]) / 360
        return hour + minutes + seconds

    def _convert_date_to_local_format2(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date
