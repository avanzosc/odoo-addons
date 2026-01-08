# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    agreement_penalty_ids = fields.One2many(
        comodel_name="agreement.penalty.type",
        inverse_name="agreement_id",
        string="Penalty Types",
    )

    active_subscription_total = fields.Integer(
        string="Active Subscriptions",
        compute="_compute_active_subscription_total",
        store=True,
    )

    @api.depends("agreement_penalty_ids.active_subscription_count")
    def _compute_active_subscription_total(self):
        for agreement in self:
            agreement.active_subscription_total = sum(
                agreement.agreement_penalty_ids.mapped("active_subscription_count")
            )
