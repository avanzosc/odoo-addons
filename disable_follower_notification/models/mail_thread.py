# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_subscribe(self, partner_ids=None, subtype_ids=None):
        return super(
            MailThread, self.with_context(mail_auto_subscribe_no_notify=True)
        ).message_subscribe(partner_ids=partner_ids, subtype_ids=subtype_ids)
