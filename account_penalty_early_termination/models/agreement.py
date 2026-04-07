# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class Agreement(models.Model):
    _inherit = "agreement"

    def apply_penalties(self):
        super().apply_penalties()
        self._apply_early_termination_penalties()

    def _apply_early_termination_penalties(self):
        for agreement in self:
            subscription_penalties = self.env["subscription.penalty"].search(
                [
                    ("subscription_id.agreement_id", "=", agreement.id),
                    ("subscription_id.stage_id.category", "=", "closed"),
                    ("penalty_type_id.name", "=", "Early Termination"),
                ]
            )

            if not subscription_penalties:
                continue

            penalty_line = agreement.agreement_penalty_ids.filtered(
                lambda l: l.penalty_type_id.name == "Early Termination"
            )[:1]

            if not penalty_line:
                continue

            penalty_quantity = len(subscription_penalties)
            penalty_amount = sum(subscription_penalties.mapped("penalty_amount"))

            if penalty_quantity <= 0 or penalty_amount <= 0:
                continue

            agreement._create_account_penalty(
                penalty_line, penalty_quantity, penalty_amount
            )
