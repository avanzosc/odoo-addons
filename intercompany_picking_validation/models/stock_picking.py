# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        if self.purchase_id:
            sale_order = self.env["sale.order"].sudo().search(
                [("auto_purchase_order_id", "=", self.purchase_id.id)])
            picking = sale_order.picking_ids[0]
            if picking:
                picking.sudo().button_force_done_detailed_operations()
                products = []
                for move_line in self.move_line_ids_without_package:
                    if move_line.product_id not in products:
                        products.append(move_line.product_id)
                        line = picking.move_line_ids_without_package.filtered(
                            lambda c: c.product_id == move_line.product_id)
                        if line and move_line.qty_done != line.qty_done:
                            line.qty_done = move_line.qty_done
                        if not line:
                            picking.move_line_ids_without_package = [(0, 0, {
                                "product_id": move_line.product_id.id,
                                "qty_done": move_line.qty_done,
                                "product_uom_id": move_line.product_uom_id.id,
                                "location_id": picking.location_id.id,
                                "location_dest_id": (
                                    picking.location_dest_id.id)})]
                for lines in picking.move_line_ids_without_package:
                    if lines.product_id not in products:
                        lines.unlink()
        return result
