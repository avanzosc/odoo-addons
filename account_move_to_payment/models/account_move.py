# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_ids = fields.Many2many(
        string="Payments",
        comodel_name="account.payment",
        compute="_compute_payment_ids",
    )
    payment_count = fields.Integer(
        string="Payments Count", compute="_compute_payment_count"
    )

    def _compute_payment_count(self):
        for move in self:
            move.payment_count = len(move.payment_ids)

    def _compute_payment_ids(self):
        for move in self:
            move.payment_ids = False
            payment = self.env["account.payment"].search([("ref", "=", move.name)])
            if payment:
                move.payment_ids = [(6, 0, payment.ids)]

    def action_view_payments(self):
        return {
            "name": _("Payments"),
            "view_mode": "tree,form",
            "res_model": "account.payment",
            "domain": [("id", "in", self.payment_ids.ids)],
            "type": "ir.actions.act_window",
            "context": self.env.context,
        }
