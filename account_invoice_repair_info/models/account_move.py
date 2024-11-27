# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    repair_order_id = fields.Many2one(
        string="Repair Order",
        comodel_name="repair.order",
        compute="_compute_repair_order_id",
        store=True,
    )

    @api.depends("repair_ids")
    def _compute_repair_order_id(self):
        for move in self:
            repair_order_id = self.env["repair.order"]
            for repair in move.repair_ids:
                repair_order_id = repair.id
            move.repair_order_id = repair_order_id
