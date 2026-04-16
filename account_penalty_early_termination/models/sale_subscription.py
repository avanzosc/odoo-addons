# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def set_close(self):
        result = super().set_close()

        for sub in self:
            if not sub.agreement_id:
                continue

            if not sub.template_id.recurring_rule_type == "monthly":
                continue

            delta = relativedelta(sub.date, sub.date_start)
            active_months = delta.years * 12 + delta.months

            agreement_penalty_line = sub.agreement_id.agreement_penalty_ids.filtered(
                lambda line: line.penalty_type_id.name == "Early Termination"
            )[:1]

            if not agreement_penalty_line:
                continue

            penalty_type_id = agreement_penalty_line.penalty_type_id.id
            penalty_percent = agreement_penalty_line.penalty_percentage
            penalty_permanence = agreement_penalty_line.number

            if active_months >= penalty_permanence:
                continue

            penalty_months = penalty_permanence - active_months
            subscription_line = sub.recurring_invoice_line_ids[:1]
            monthly_price = subscription_line.price_unit if subscription_line else 0.0

            if monthly_price <= 0:
                continue

            penalty_amount = penalty_percent * penalty_months * monthly_price

            if penalty_amount <= 0:
                continue

            self.env["subscription.penalty"].create(
                {
                    "subscription_id": sub.id,
                    "penalty_type_id": penalty_type_id,
                    "applied_date": fields.Date.today(),
                    "penalty_months": penalty_months,
                    "penalty_amount": penalty_amount,
                    "monthly_price": monthly_price,
                }
            )

        return result
