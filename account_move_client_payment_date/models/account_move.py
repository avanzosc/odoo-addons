# Copyright 2025 Unai Beristain - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    client_payment_date = fields.Date(
        help="Date when the client is expected to make the payment.",
    )
