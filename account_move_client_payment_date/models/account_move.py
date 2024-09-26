from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    client_payment_date = fields.Date(
        help="Date when the client is expected to make the payment.",
    )
