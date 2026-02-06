# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _early_termination_penalties(
        self, penalty_type_id, penalty_percent, penalty_permanence
    ):
        self.ensure_one()
        quantity = 0
        amount = 0.0

        if not self.date or self.stage_id.category != "closed":
            return {"quantity": quantity, "amount": amount}

        if self.env["subscription.penalty"].search(
            [
                ("subscription_id", "=", self.id),
                ("penalty_type_id", "=", penalty_type_id),
            ],
            limit=1,
        ):
            return {"quantity": quantity, "amount": amount}

        start_date = self.date_start
        end_date = self.date
        delta = relativedelta(end_date, start_date)
        active_months = delta.years * 12 + delta.months

        if active_months >= penalty_permanence:
            return {"quantity": quantity, "amount": amount}

        penalty_months = penalty_permanence - active_months
        subscription_line = self.recurring_invoice_line_ids[:1]
        monthly_price = subscription_line.price_unit if subscription_line else 0.0

        if monthly_price <= 0:
            return {"quantity": quantity, "amount": amount}

        penalty_amount = penalty_percent * penalty_months * monthly_price / 100.0
        if penalty_amount <= 0:
            return {"quantity": quantity, "amount": amount}

        self.env["subscription.penalty"].create(
            {
                "subscription_id": self.id,
                "penalty_type_id": penalty_type_id,
                "applied_date": fields.Date.today(),
            }
        )

        quantity += 1
        amount += penalty_amount

        return {"quantity": quantity, "amount": amount}
