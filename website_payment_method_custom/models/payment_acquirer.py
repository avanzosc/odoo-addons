
from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    website_payment_btn_text = fields.Char("Website payment button text")
