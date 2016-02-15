# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    start_time = fields.Float(string='Start time')
    end_time = fields.Float(string='End time')

    def _update_registration_start_date(self, registration):
        from_date = self._convert_date_to_local_format(self.from_date).date()
        registration.date_start = self._put_utc_format_date(
            from_date, self.start_time)

    def _update_registration_date_end(self, registration):
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
                '|', ('date', '=', False), '&',
                ('date', '>=', self.from_date),
                ('date', '<=', self.to_date)]
        return cond
