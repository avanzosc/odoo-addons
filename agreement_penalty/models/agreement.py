# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    agreement_penalty_ids = fields.One2many(
        comodel_name="agreement.penalty.type",
        inverse_name="agreement_id",
        string="Penalties",
    )

    penalty_ids = fields.One2many(
        comodel_name="account.penalty",
        inverse_name="agreement_id",
        string="Penalties",
    )

    penalty_count = fields.Integer(string="Penalties", compute="_compute_penalty_count")

    def _compute_penalty_count(self):
        for rec in self:
            rec.penalty_count = len(rec.penalty_ids)

    def action_open_penalties(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Penalties",
            "res_model": "account.penalty",
            "view_mode": "tree,form",
            "domain": [("agreement_id", "=", self.id)],
            "context": {"default_agreement_id": self.id},
        }
