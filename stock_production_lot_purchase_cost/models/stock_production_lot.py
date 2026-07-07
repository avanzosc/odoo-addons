# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.lot"

    purchase_cost = fields.Float(compute="_compute_purchase_cost")

    def _compute_purchase_cost(self):
        for lot in self:
            cost = 0
            lines = self.env["stock.move.line"].search(
                [
                    ("lot_id", "=", lot.id),
                    ("picking_code", "=", "incoming"),
                    ("state", "=", "done"),
                ]
            )
            if lines and sum(lines.mapped("quantity")) != 0:
                cost = sum(lines.mapped("cost")) / sum(lines.mapped("quantity"))
            lot.purchase_cost = cost
