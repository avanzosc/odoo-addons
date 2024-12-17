# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def action_divide(self):
        result = super().action_divide()
        if (
            self.product_id
            and self.product_id.tracking != "none"
            and self.picking_id
            and self.picking_id.picking_type_id
            and self.picking_id.picking_type_id.use_create_lots
        ):
            for line in self.move_id.move_line_ids:
                line.lot_name = self.env["ir.sequence"].next_by_code("stock.lot.serial")
        return result
