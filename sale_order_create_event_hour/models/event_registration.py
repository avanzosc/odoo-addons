# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    def _prepare_wizard_registration_open_vals(self):
        wiz_vals = super(EventRegistration,
                         self)._prepare_wizard_registration_open_vals()
        start_time = self._convert_times_to_float(self.event_id.date_begin)
        end_time = self._convert_times_to_float(self.event_id.date_end)
        wiz_vals.update({'start_time': start_time,
                         'end_time': end_time,
                         'min_from_date': self.event_id.date_begin,
                         'max_to_date': self.event_id.date_end})
        return wiz_vals

    def _prepare_date_start_for_track_condition(self, date):
        new_date = self._convert_date_to_local_format(date).date()
        start_time = self._convert_times_to_float(self.event_id.date_begin)
        new_date = self._put_utc_format_date(
            new_date, start_time).strftime('%Y-%m-%d %H:%M:%S')
        return new_date

    def _prepare_date_end_for_track_condition(self, date):
        new_date = self._convert_date_to_local_format(date).date()
        end_time = self._convert_times_to_float(self.event_id.date_end)
        new_date = self._put_utc_format_date(
            new_date, end_time).strftime('%Y-%m-%d %H:%M:%S')
        return new_date

    def _prepare_wizard_reg_cancel_vals(self):
        wiz_vals = super(EventRegistration,
                         self)._prepare_wizard_reg_cancel_vals()
        start_time = self._convert_times_to_float(self.event_id.date_begin)
        end_time = self._convert_times_to_float(self.event_id.date_end)
        wiz_vals.update({'start_time': start_time,
                         'end_time': end_time,
                         'min_from_date': self.event_id.date_begin,
                         'max_to_date': self.event_id.date_end})
        return wiz_vals

    def _convert_times_to_float(self, date):
        minutes = 0.0
        seconds = 0.0
        local_time = self._convert_date_to_local_format(
            date).strftime("%H:%M:%S")
        time = local_time.split(':')
        hour = float(time[0])
        if int(time[1]) > 0:
            minutes = float(time[1]) / 60
        if int(time[2]) > 0:
            seconds = float(time[2]) / 360
        return hour + minutes + seconds
