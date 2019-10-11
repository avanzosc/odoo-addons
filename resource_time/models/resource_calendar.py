# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from pytz import timezone, utc

from odoo import api, fields, models


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    hour_gap = fields.Float(
        string='Weekly Hour Gap', compute='_compute_hour_gap')

    @api.depends('attendance_ids', 'attendance_ids.hour_from',
                 'attendance_ids.hour_to', 'attendance_ids.dayofweek',
                 'attendance_ids.date_from', 'attendance_ids.date_to')
    def _compute_hour_gap(self):
        today = fields.Date.context_today(self)
        year, week_num, day_of_week = today.isocalendar()
        start_dt = datetime.strptime(
            '{}-W{}-1'.format(year, week_num-1), "%Y-W%W-%w").replace(
            tzinfo=utc)
        end_dt = start_dt + timedelta(days=7, seconds=-1)
        for record in self:
            # Set timezone in UTC if no timezone is explicitly given
            if record.tz:
                tz = timezone((record or self).tz)
                start_dt = start_dt.replace(tzinfo=tz)
                end_dt = end_dt.replace(tzinfo=tz)
            record.hour_gap = record.get_work_hours_count(
                start_dt, end_dt, compute_leaves=False)


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    hour_gap = fields.Float(
        string='Hour Gap', compute='_compute_hour_gap', store=True)

    @api.depends('hour_from', 'hour_to')
    def _compute_hour_gap(self):
        for record in self:
            record.hour_gap = record.hour_to - record.hour_from
