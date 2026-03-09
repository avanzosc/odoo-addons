# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    subscription_penalty_ids = fields.One2many(
        "subscription.penalty", "subscription_id", string="Penalties"
    )
