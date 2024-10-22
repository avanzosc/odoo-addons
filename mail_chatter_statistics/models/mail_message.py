from odoo import models, fields

class MailMessage(models.Model):
    _inherit = "mail.message"

    mailing_trace_ids = fields.One2many(
        comodel_name="mailing.trace",
        inverse_name="mail_message_id",
        string="Mailing Traces",
        help="Mailing traces related to this message.",
    )
