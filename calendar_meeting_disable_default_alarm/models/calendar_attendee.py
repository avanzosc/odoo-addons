import logging

from odoo import models

_logger = logging.getLogger(__name__)


class Attendee(models.Model):
    _inherit = "calendar.attendee"

    def _send_mail_to_attendees(
        self, template_xmlid, force_send=False, ignore_recurrence=False
    ):
        if self._context.get("no_mail_to_attendees"):
            _logger.info("No mail will be sent to attendees due to context flag.")
            return False

        return super(Attendee, self)._send_mail_to_attendees(
            template_xmlid, force_send, ignore_recurrence
        )
