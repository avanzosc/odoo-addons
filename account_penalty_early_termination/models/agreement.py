# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    def apply_penalties(self):
        super().apply_penalties()
        self._apply_early_termination_penalties()

    def _apply_early_termination_penalties(self):
        for agreement in self:

            if agreement._check_existing_month_penalty("Early Termination"):
                continue

            today = fields.Date.today()
            first_day_this_month = today.replace(day=1)
            first_day_prev_month = first_day_this_month - relativedelta(months=1)

            subscription_penalties = self.env["subscription.penalty"].search(
                [
                    ("subscription_id.agreement_id", "=", agreement.id),
                    ("subscription_id.stage_id.category", "=", "closed"),
                    ("penalty_type_id.name", "=", "Early Termination"),
                    ("applied_date", ">=", first_day_prev_month),
                    ("applied_date", "<", first_day_this_month),
                ]
            )

            if not subscription_penalties:
                continue

            penalty_line = agreement.agreement_penalty_ids.filtered(
                lambda l: l.penalty_type_id.name == "Early Termination"
            )[:1]

            if not penalty_line:
                continue

            affected_subscription = len(subscription_penalties)
            penalty_amount = sum(subscription_penalties.mapped("penalty_amount"))

            if penalty_amount <= 0:
                continue

            agreement._create_account_penalty(
                penalty_line, penalty_amount, affected_subscription
            )
