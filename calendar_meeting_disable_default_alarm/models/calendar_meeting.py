from odoo import _, fields, models
from odoo.exceptions import UserError


class CalendarMeeting(models.Model):
    _inherit = "calendar.event"

    def write(self, values):
        detached_events = self.env["calendar.event"]
        recurrence_update_setting = values.pop("recurrence_update", None)
        update_recurrence = (
            recurrence_update_setting in ("all_events", "future_events")
            and len(self) == 1
        )
        break_recurrence = values.get("recurrency") is False

        update_alarms = False
        update_time = False
        if "partner_ids" in values:
            values["attendee_ids"] = self._attendees_values(values["partner_ids"])
            update_alarms = True

        time_fields = self.env["calendar.event"]._get_time_fields()
        if any(values.get(key) for key in time_fields) or "alarm_ids" in values:
            update_alarms = True
            update_time = True

        if (
            not recurrence_update_setting
            or recurrence_update_setting == "self_only"
            and len(self) == 1
        ) and "follow_recurrence" not in values:
            if any(
                {field: values.get(field) for field in time_fields if field in values}
            ):
                values["follow_recurrence"] = False

        previous_attendees = self.attendee_ids

        recurrence_values = {
            field: values.pop(field)
            for field in self._get_recurrent_fields()
            if field in values
        }
        if update_recurrence:
            if break_recurrence:
                # Update this event
                detached_events |= self._break_recurrence(
                    future=recurrence_update_setting == "future_events"
                )
            else:
                update_start = (
                    self.start if recurrence_update_setting == "future_events" else None
                )
                time_values = {
                    field: values.pop(field) for field in time_fields if field in values
                }
                if not update_start and (time_values or recurrence_values):
                    raise UserError(
                        _(
                            "Updating All Events is not allowed when dates or time is modified.\
                                  You can only update one particular event and following events."
                        )
                    )
                detached_events |= self._split_recurrence(time_values)
                self.recurrence_id._write_events(values, dtstart=update_start)
        else:
            super().write(values)
            self._sync_activities(fields=values.keys())

        # We reapply recurrence for future events and
        # when we add a rrule and 'recurrency' == True on the event
        if (
            recurrence_update_setting not in ["self_only", "all_events"]
            and not break_recurrence
        ):
            detached_events |= self._apply_recurrence_values(
                recurrence_values, future=recurrence_update_setting == "future_events"
            )

        (detached_events & self).active = False
        (detached_events - self).with_context(archive_on_error=True).unlink()

        # Notify attendees if there is an alarm on the modified event, or if there was an alarm
        # that has just been removed, as it might have changed their next event notification
        if not self.env.context.get("dont_notify") and update_alarms:
            self.env["calendar.alarm_manager"]._notify_next_alarm(self.partner_ids.ids)
        attendee_update_events = self.filtered(lambda ev: ev.user_id != self.env.user)
        if update_time and attendee_update_events:
            # Another user update the event time fields. It should not be auto accepted for the organizer.
            # This prevent weird behavior when a user modified future events time fields and
            # the base event of a recurrence is accepted by the organizer but not the following events
            attendee_update_events.attendee_ids.filtered(
                lambda att: self.user_id.partner_id == att.partner_id
            ).write({"state": "needsAction"})

        current_attendees = self.filtered("active").attendee_ids
        # if 'partner_ids' in values:
        #     (current_attendees - previous_attendees).\
        #       _send_mail_to_attendees('calendar.calendar_template_meeting_invitation')
        if not self.env.context.get("is_calendar_event_new") and "start" in values:
            start_date = fields.Datetime.to_datetime(values.get("start"))
            # Only notify on future events
            if start_date and start_date >= fields.Datetime.now():
                (current_attendees & previous_attendees)._send_mail_to_attendees(
                    "calendar.calendar_template_meeting_changedate",
                    ignore_recurrence=not update_recurrence,
                )

        return True
