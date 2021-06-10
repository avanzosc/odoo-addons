# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from dateutil.relativedelta import relativedelta
import pytz


class EventEvent(models.Model):
    _inherit = 'event.event'

    def write(self, vals):
        my_stage = self.env.ref('event.event_stage_announced')
        res = super(EventEvent, self).write(vals)
        if vals.get('stage_id', False):
            stage = self.env['event.stage'].browse(vals['stage_id'])
            if stage == my_stage:
                for event in self:
                    event._create_tracks()
        return res

    def _create_tracks(self):
        timezone = pytz.timezone(self.date_tz or 'UTC')
        date_start = self.date_begin
        date_start = date_start.replace(
            tzinfo=pytz.timezone('UTC')).astimezone(timezone)
        date_start = date_start.date()
        date_end = self.date_end
        date_end = date_end.replace(
            tzinfo=pytz.timezone('UTC')).astimezone(timezone)
        date_end = date_end.date()
        n = 1
        while date_start <= date_end:
            day = date_start.weekday()
            lines = self.resource_calendar_id.attendance_ids.filtered(
                lambda x: x.dayofweek == str(day))
            for line in lines:
                track_vals = self.catch_values_for_track(line, date_start, n)
                n = n+1
                self.env['event.track'].create(track_vals)
            date_start = date_start + relativedelta(days=1)

    def catch_values_for_track(self, line, date_start, n):
        my_hours = '{0:02.0f}:{1:02.0f}'.format(
            *divmod(line.hour_from * 60, 60))
        my_date = '{} {}:00'.format(date_start, my_hours)
        my_date = fields.Datetime.from_string(my_date)
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        my_date = timezone.localize(my_date).astimezone(pytz.UTC)
        my_date = my_date.replace(tzinfo=None)
        track_vals = {
            'name': _('Session {}').format(n),
            'date': my_date,
            'duration': line.hour_to-line.hour_from,
            'event_id': self.id,
            'user_id': self.env.user.id,
            'address_id': self.address_id.id,
            'partner_id': self.main_responsible_id.partner_id.id,
            'second_responsible_id': self.second_responsible_id.partner_id.id}
        return track_vals
