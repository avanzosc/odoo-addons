# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    purchase_cost = fields.Float(
        string="Purchase Cost", compute="_compute_purchase_cost"
    )

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
            if lines and sum(lines.mapped("qty_done")) != 0:
                cost = sum(lines.mapped("amount")) / sum(lines.mapped("qty_done"))
            lot.purchase_cost = cost
