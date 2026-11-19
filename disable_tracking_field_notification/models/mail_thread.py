# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_track(self, tracked_fields, initial):
        tracked_fields = {}
        initial = {}
        return super()._message_track(tracked_fields, initial)
