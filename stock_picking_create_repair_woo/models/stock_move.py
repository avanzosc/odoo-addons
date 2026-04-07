# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        result = super().write(vals)
        if "product_id" not in vals:
            return result
        moves = self.filtered(
            lambda m: (
                m.picking_type_id.code == "incoming"
                and m.picking_id.is_repair
                and not m.product_id.generic_repair_product
                and m.sale_line_id
                and m.sale_line_id.product_to_repair_id.generic_repair_product
            )
        )
        for move in moves:
            move.sale_line_id.product_to_repair_id = move.product_id.id
        return result
