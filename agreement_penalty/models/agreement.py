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

    def _get_penalty_journal(self):
        self.ensure_one()
        return (
            self.sale_type_id.journal_id
            if self.sale_type_id and self.sale_type_id.journal_id
            else self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        )

    def _create_account_penalty(self, penalty_line, quantity, amount):
        self.ensure_one()
        self.env["account.penalty"].create(
            {
                "agreement_id": self.id,
                "name": penalty_line.penalty_type_id.name,
                "quantity": quantity,
                "amount": amount,
                "invoice_date": fields.Date.today(),
                "penalty_type_id": penalty_line.penalty_type_id.id,
                "product_id": penalty_line.penalty_type_id.product_id.id
                if penalty_line.penalty_type_id.product_id
                else False,
                "partner_id": self.partner_id.id if self.partner_id else False,
                "journal_id": self._get_penalty_journal().id,
            }
        )

    def apply_penalties(self):
        return
