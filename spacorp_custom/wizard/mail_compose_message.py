# Copyright 2023 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class MailComposerMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self):
        if (
            "active_model" in self.env.context
            and self.env.context.get("active_model", "a") == "stock.picking"
        ):
            pickings = self.env["stock.picking"].browse(
                self.env.context.get("active_id")
            )
            for picking in pickings:
                picking.confirmation_email_sent = True
        return super().action_send_mail()
