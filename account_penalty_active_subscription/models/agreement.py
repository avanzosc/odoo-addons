# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class Agreement(models.Model):
    _inherit = "agreement"

    def apply_penalties(self):
        super().apply_penalties()
        self._apply_active_subscription_penalties()

    def _apply_active_subscription_penalties(self):
        for agreement in self:
            active_count = self.env["sale.subscription"].search_count(
                [
                    ("agreement_id", "=", agreement.id),
                    ("date", "=", False),
                    ("stage_id.category", "=", "progress"),
                ]
            )

            penalty_line = agreement.agreement_penalty_ids.filtered(
                lambda l: l.penalty_type_id.name == "Active Subscriptions"
            )[:1]

            if not penalty_line:
                continue

            penalty_quantity = penalty_line.active_subscription_count - active_count

            if penalty_quantity <= 0 or not penalty_line.penalty_type_id.product_id:
                continue

            penalty_amount = (
                penalty_line.penalty_percentage
                * penalty_line.penalty_type_id.product_id.list_price
                * penalty_quantity
            )

            if penalty_amount <= 0:
                continue

            agreement._create_account_penalty(
                penalty_line, penalty_quantity, penalty_amount
            )
