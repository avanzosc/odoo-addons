# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    machine_ids = fields.One2many(
        string="Machines",
        comodel_name="machine",
        inverse_name="purch_inv_id",
    )
    machine_count = fields.Integer(
        compute="_compute_machine_count",
    )

    @api.depends("machine_ids")
    def _compute_machine_count(self):
        for move in self:
            move.machine_count = len(move.machine_ids)

    def action_post(self):
        result = super().action_post()
        for move in self.filtered(
            lambda x: x.move_type == "in_invoice" and x.invoice_origin
        ):
            purchase = self.env["purchase.order"].search(
                [("name", "=", move.invoice_origin)], limit=1
            )
            if purchase:
                machines = self.env["machine"].search(
                    [
                        ("purchase_id", "=", purchase.id),
                        ("purch_inv_id", "=", False),
                    ]
                )
                machines.write({"purch_inv_id": move.id})
        return result
