# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SubscriptionPenalty(models.Model):
    _name = "subscription.penalty"
    _description = "Subscription Penalty"

    subscription_id = fields.Many2one(
        "sale.subscription", string="Subscription", ondelete="cascade"
    )

    penalty_type_id = fields.Many2one(
        "penalty.type",
        string="Penalty Type",
    )

    applied_date = fields.Date()
