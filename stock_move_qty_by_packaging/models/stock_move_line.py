# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _compute_boxes_sacs(self):
        for line in self:
            if line.picking_id.state != "done":
                qty = line.reserved_uom_qty
            else:
                qty = line.qty_done
            boxes_sacks = 0
            if (
                line.move_id
                and line.move_id.sale_line_id
                and line.move_id.sale_line_id.product_packaging_qty
            ):
                sale_line = line.move_id.sale_line_id
                packaging_qty = sale_line.product_packaging_qty
                product_uom_qty = sale_line.product_uom_qty
                boxes_sacks = (qty * packaging_qty) / product_uom_qty
            line.boxes_sacks = boxes_sacks

    boxes_sacks = fields.Integer(string="Boxes/Sacks", compute="_compute_boxes_sacs")

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        out_picking_lines = self.filtered(lambda x: x.picking_code == "outgoing")
        if not result or len(self) != len(out_picking_lines):
            return result
        for clave in result.keys():
            for move_line in self.filtered(
                lambda x: x.move_id
                and x.qty_done
                and x.move_id.sale_line_id
                and x.move_id.sale_line_id.product_packaging_qty
            ):
                line_key = self._generate_keys_to_found()
                if line_key in clave:
                    boxes_sacks = move_line._get_boxes_sacks()
                    result[clave]["boxes_sacks"] = round(boxes_sacks,2)
        return result

    def _generate_keys_to_found(self):
        uom = self.product_uom_id
        name = self.product_id.display_name
        description = self.move_id.description_picking
        product = self.product_id
        if description == name or description == self.product_id.name:
            description = False
        line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}'
        return line_key

    def _get_boxes_sacks(self):
        sale_line = self.move_id.sale_line_id
        packaging_qty = sale_line.product_packaging_qty
        product_uom_qty = sale_line.product_uom_qty
        uom = self.product_uom_id
        qty_done = self.product_uom_id._compute_quantity(self.qty_done, uom)
        boxes_sacks = (qty_done * packaging_qty) / product_uom_qty
        return boxes_sacks
