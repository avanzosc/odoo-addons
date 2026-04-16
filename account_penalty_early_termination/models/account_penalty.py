# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Penalty(models.Model):
    _inherit = "account.penalty"

    is_early_termination = fields.Boolean(compute="_compute_is_early_termination")

    def _compute_is_early_termination(self):
        for penalty in self:
            penalty.is_early_termination = (
                penalty.penalty_type_id.name == "Early Termination"
            )

    def action_view_subscription_penalties(self):
        self.ensure_one()
        base_date = self.invoice_date
        first_day_this_month = base_date.replace(day=1)
        first_day_prev_month = first_day_this_month - relativedelta(months=1)
        action = self.env.ref(
            "subscription_penalty.action_subscription_penalty"
        ).read()[0]
        action["domain"] = [
            ("applied_date", ">=", first_day_prev_month),
            ("applied_date", "<", first_day_this_month),
            ("subscription_id.agreement_id", "=", self.agreement_id.id),
        ]
        return action
