# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields
from datetime import datetime
from pytz import timezone, utc


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    def _prepare_wizard_registration_open_vals(self):
        wiz_vals = super(EventRegistration,
                         self)._prepare_wizard_registration_open_vals()
        wiz_vals = self._update_wizard_vals(wiz_vals)
        return wiz_vals

    def _prepare_wizard_reg_cancel_vals(self):
        wiz_vals = super(EventRegistration,
                         self)._prepare_wizard_reg_cancel_vals()
        wiz_vals = self._update_wizard_vals(wiz_vals)
        return wiz_vals

    def _update_wizard_vals(self, wiz_vals):
        if self.date_start:
            start_time = self._convert_times_to_float(self.date_start)
            wiz_vals.update({'from_date': self._convert_date_to_local_format2(
                             self.date_start).date(),
                             'min_from_date': self.date_start})
        else:
            start_time = self._convert_times_to_float(self.event_id.date_begin)
            wiz_vals.update({'from_date': self._convert_date_to_local_format2(
                             self.event_id.date_begin).date(),
                             'min_from_date': self.event_id.date_begin})
        if self.date_end:
            end_time = self._convert_times_to_float(self.date_end)
            wiz_vals.update({'to_date': self._convert_date_to_local_format2(
                             self.date_end).date(),
                             'max_to_date': self.date_end})
        else:
            end_time = self._convert_times_to_float(self.event_id.date_end)
            wiz_vals.update({'to_date': self._convert_date_to_local_format2(
                             self.event_id.date_end).date(),
                             'max_to_date': self.event_id.date_end})
        wiz_vals.update({'start_time': start_time,
                         'end_time': end_time})
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

    def _convert_date_to_local_format2(self, date):
        new_date = fields.Datetime.from_string(date).date()
        local_date = datetime(
            int(new_date.strftime("%Y")), int(new_date.strftime("%m")),
            int(new_date.strftime("%d")), int(date[11:13]), int(date[14:16]),
            int(date[17:19]), tzinfo=utc).astimezone(
            timezone(self.env.user.tz)).replace(tzinfo=None)
        return local_date
