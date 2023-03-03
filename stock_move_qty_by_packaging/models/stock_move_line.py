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
            if (line.move_id and line.move_id.sale_line_id and
                    line.move_id.sale_line_id.product_packaging_qty):
                sale_line = line.move_id.sale_line_id
                packaging_qty = sale_line.product_packaging_qty
                product_uom_qty = sale_line.product_uom_qty
                boxes_sacks = ((qty * packaging_qty) / product_uom_qty)
            line.boxes_sacks = boxes_sacks

    boxes_sacks = fields.Integer(
        string="Boxes/Sacks", compute="_compute_boxes_sacs")

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super(
            StockMoveLine, self)._get_aggregated_product_quantities(**kwargs)
        out_picking_lines = self.filtered(
            lambda x: x.picking_code == 'outgoing')
        if len(self) != len(out_picking_lines):
            return result
        aggregated_move_lines = {}
        for move_line in self:
            name = move_line.product_id.display_name
            description = move_line.move_id.description_picking
            if description == name or description == move_line.product_id.name:
                description = False
            uom = move_line.product_uom_id
            line_key = (str(move_line.product_id.id) + "_" + name +
                        (description or "") + "uom " + str(uom.id))
            if line_key in aggregated_move_lines:
                boxes_sacks = 0
                if (move_line.move_id and move_line.sale_line_id and
                        move_line.sale_line_id.product_packaging_qty):
                    sale_line = move_line.sale_line_id
                    packaging_qty = sale_line.product_packaging_qty
                    product_uom_qty = sale_line.product_uom_qty
                    qty_done = move_line.product_uom_id._compute_quantity(
                        move_line.qty_done, uom)
                    boxes_sacks = (
                        (qty_done * packaging_qty) / product_uom_qty)
                aggregated_move_lines[line_key]['boxes_sacks'] = boxes_sacks
        return aggregated_move_lines
