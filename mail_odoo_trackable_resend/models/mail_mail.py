from odoo import fields, models


class MailMail(models.Model):
    _inherit = "mail.mail"

    received = fields.Boolean(
        string="Recibido",
        default=False,
    )
    opened = fields.Boolean(
        string="Abierto",
        default=False,
    )
    click_count = fields.Integer(
        string="Número de clics",
        default=0,
    )
