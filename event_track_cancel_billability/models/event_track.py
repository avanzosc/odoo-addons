# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventTrack(models.Model):
    _inherit = "event.track"

    notice_deadline = fields.Datetime(
        string="Notice Deadline",
        compute="_compute_notice_deadline",
    )
    cancelled_company = fields.Boolean(
        string="Cancelled By Company",
        default=False,
    )
    payable = fields.Float(
        string="Payable",
        compute="_compute_payable",
        store=True,
    )
    billable = fields.Float(
        string="Billable",
        compute="_compute_billable",
        store=True,
    )

    @api.depends("time_type_id")
    def _compute_payable(self):
        types = self.env.ref("event_track_cancel_reason.time_type1")
        types |= self.env.ref("event_track_cancel_reason.time_type2")
        for track in self:
            track.payable = 0.0
            if track.time_type_id in types:
                track.payable = track.duration

    @api.depends("time_type_id")
    def _compute_billable(self):
        types = self.env.ref("event_track_cancel_reason.time_type1")
        types |= self.env.ref("event_track_cancel_reason.time_type2")
        types |= self.env.ref("event_track_cancel_reason.time_type3")
        for track in self:
            track.billable = 0.0
            if track.time_type_id in types:
                track.billable = track.duration

    @api.onchange("cancelled_company")
    def onchange_cancelled_company(self):
        if self.cancelled_company:
            self.time_type_id = self.env.ref("event_track_cancel_reason.time_type4").id
        else:
            self.time_type_id = self.env.ref("event_track_cancel_reason.time_type1").id

    @api.depends("date", "event_id.hours_advance", "event_id.customer_service_id")
    def _compute_notice_deadline(self):
        for track in self:
            if (
                track.date
                and (track.event_id.hours_advance)
                and (track.event_id.customer_service_id)
            ):
                timezone = pytz.timezone(track.event_id.date_tz or "UTC")
                event_date = track.date
                event_date = event_date.replace(tzinfo=pytz.timezone("UTC")).astimezone(
                    timezone
                )
                attendance = track.event_id.customer_service_id.attendance_ids
                global_leaves = track.event_id.customer_service_id.global_leave_ids
                holidays = []
                for days in global_leaves:
                    date_from = days.date_from.date()
                    date_to = days.date_to.date()
                    while date_from <= date_to:
                        holidays.append(date_from)
                        date_from = +timedelta(days=1)
                day = attendance.filtered(
                    lambda x: x.dayofweek == str(event_date.weekday())
                )
                if len(day) > 1:
                    raise ValidationError(
                        _("Customer service hours are a split schedule")
                    )
                n = 1
                track_hour = True
                while not day.id:
                    event_date = event_date - timedelta(days=n)
                    day = attendance.filtered(
                        lambda x: x.dayofweek == str(event_date.weekday())
                    )
                    if len(day) > 1:
                        raise ValidationError(
                            _("Customer service hours are a split schedule")
                        )
                    track_hour = False
                first_hour = day.hour_from - 2
                first_hour = "{:02.0f}:{:02.0f}".format(*divmod(first_hour * 60, 60))
                first_hour = "{} {}:00".format(event_date.date(), first_hour)
                first_hour = fields.Datetime.from_string(first_hour)
                first_hour = first_hour.replace(tzinfo=pytz.timezone("UTC")).astimezone(
                    timezone
                )
                if not first_hour:
                    raise ValidationError(
                        _("The day of the track is not in the customer " + "service.")
                    )
                else:
                    before_day = event_date.date() - timedelta(days=1)
                    while not attendance.filtered(
                        lambda x: x.dayofweek == str(before_day.weekday())
                    ) or (before_day in holidays):
                        before_day = before_day - timedelta(days=1)
                    last_hour = (
                        attendance.filtered(
                            lambda x: x.dayofweek == str(before_day.weekday())
                        ).hour_to
                        - 2
                    )
                    last_hour = "{:02.0f}:{:02.0f}".format(*divmod(last_hour * 60, 60))
                    hour = "{} {}:00".format(event_date.date(), last_hour)
                    hour = fields.Datetime.from_string(hour)
                    hour = hour.replace(tzinfo=pytz.timezone("UTC")).astimezone(
                        timezone
                    )
                    if track_hour is False or hour.time() < event_date.time():
                        event_date = "{} {}:00".format(event_date.date(), last_hour)
                        event_date = fields.Datetime.from_string(event_date)
                        event_date = event_date.replace(
                            tzinfo=pytz.timezone("UTC")
                        ).astimezone(timezone)
                    last_hour = "{} {}:00".format(before_day, last_hour)
                    last_hour = fields.Datetime.from_string(last_hour)
                    last_hour = last_hour.replace(
                        tzinfo=pytz.timezone("UTC")
                    ).astimezone(timezone)
                    missing_hours = track.event_id.hours_advance
                    missing_hours = timedelta(hours=missing_hours)
                    deadline = event_date - missing_hours
                    if deadline >= first_hour:
                        deadline = deadline.astimezone(pytz.UTC).replace(tzinfo=None)
                        track.notice_deadline = deadline
                    else:
                        if event_date > first_hour:
                            missing_hours = missing_hours - (event_date - first_hour)
                        deadline = last_hour - missing_hours
                        deadline = deadline.astimezone(pytz.UTC).replace(tzinfo=None)
                        track.notice_deadline = deadline
            else:
                self.notice_deadline = False
