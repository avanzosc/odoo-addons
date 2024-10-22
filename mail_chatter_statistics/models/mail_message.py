from odoo import api, fields, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    mailing_trace_ids = fields.One2many(
        comodel_name="mailing.trace",
        inverse_name="mail_message_id",
        string="Mailing Traces",
        help="Mailing traces related to this message.",
    )

    mail_notification_ids = fields.One2many(
        comodel_name="mail.notification",
        inverse_name="mail_message_id",
        string="Mailing Notifications",
        help="Mailing notifications related to this message.",
    )

    @api.model
    def message_process_incoming(self, message, message_dict):
        super(MailMessage, self).message_process_incoming(message, message_dict)

        thread_references = message_dict.get("references") or message_dict.get(
            "in_reply_to"
        )
        msg_references = (
            tools.mail_header_msgid_re.findall(thread_references)
            if thread_references
            else []
        )

        if msg_references:
            self.env["mailing.trace"].set_opened(mail_message_ids=msg_references)
            self.env["mailing.trace"].set_replied(mail_message_ids=msg_references)

    @api.model
    def get_mailing_trace(self, mail_message_id):
        mail_message_id = int(mail_message_id)
        mailing_trace = self.env["mailing.trace"].search(
            [("mail_message_id", "=", mail_message_id)], limit=1
        )

        if mailing_trace:
            # Return dictionary representation of mailing_trace
            return mailing_trace.read(
                [
                    "id",
                    "sent_at",
                    "clicked_at",
                    "opened_at",
                    "bounced_at",
                    "replied_at",
                    "user_agent",
                ]
            )[0]
        return False
