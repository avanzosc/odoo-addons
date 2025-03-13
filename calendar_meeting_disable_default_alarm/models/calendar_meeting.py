from odoo import models


class CalendarMeeting(models.Model):
    _inherit = "calendar.event"

    def write(self, values):
        context = dict(self.env.context)

        # 'dont_notify' is a flag used by Odoo core to prevent sending emails
        # This is applied, for example, in the following code where it avoids
        # notifying users about alarms:
        # if not self.env.context.get('dont_notify') and update_alarms:
        #     self.env['calendar.alarm_manager'].
        #           _notify_next_alarm(self.partner_ids.ids)

        # 'no_mail_to_attendees' is a custom flag in this module that prevents
        # sending emails to attendees when an event is modified. This affects
        # the '_send_mail_to_attendees' function to prevent emails when new
        # attendees are added or event details are modified.
        context.update({"dont_notify": True, "no_mail_to_attendees": True})

        return super(CalendarMeeting, self.with_context(context)).write(values)
