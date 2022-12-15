# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_name_to_print = fields.Char(
        string="Product name to print",
        compute="_compute_product_name_to_print")

    def _compute_product_name_to_print(self):
        for line in self:
            name = line.product_id.name
            if line.product_id.default_code:
                name = "[{}] {}".format(
                    line.product_id.default_code, line.product_id.name)
            if line.move_id.product_customer_code:
                name = "[{}] {}".format(
                    line.move_id.product_customer_code, line.product_id.name)
            line.product_name_to_print = name

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
            name = move_line.product_id.name
            if move_line.product_id.default_code:
                name = "[{}] {}".format(
                    move_line.product_id.default_code,
                    move_line.product_id.name)
            if move_line.move_id.product_customer_code:
                name = "[{}] {}".format(
                    move_line.move_id.product_customer_code,
                    move_line.product_id.name)
            if line_key not in aggregated_move_lines:
                aggregated_move_lines[line_key] = {
                    'name': name,
                    'description': "",
                    'qty_done': move_line.qty_done,
                    'product_uom': uom.name,
                    'product_uom_rec': uom,
                    'product': move_line.product_id}
            else:
                aggregated_move_lines[line_key]['qty_done'] += move_line.qty_done
        return aggregated_move_lines
