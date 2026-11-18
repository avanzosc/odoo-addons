# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountPaymentMode(models.Model):
    _inherit = "account.payment.mode"

    payment_days_basis = fields.Selection(
        selection=[
            ("payment", "Payment Date"),
            ("due", "Due Date"),
        ],
        string="Calculate Average Using",
        default="due",
        required=True,
        help="Date used to calculate the number of days since the accounting date.",
    )
