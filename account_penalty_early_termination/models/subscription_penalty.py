# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SubscriptionPenalty(models.Model):
    _inherit = "subscription.penalty"

    penalty_months = fields.Integer(
        string="Penalty Months",
    )
    penalty_amount = fields.Float(
        string="Penalty Amount",
        digits=(16, 2),
    )
    monthly_price = fields.Float(
        string="Monthly Price",
        digits=(16, 2),
    )
