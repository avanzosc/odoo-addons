# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _compute_product_display_name(self):
        for line in self:
            product_display_name = line.product_id.display_name
            if (line.picking_id.picking_type_id.code == "outgoing" and
                line.product_id.default_code and
                line.move_id.customer_product_code and
                    line.product_id.default_code in product_display_name):
                new_value = product_display_name.replace(
                    line.product_id.default_code,
                    line.move_id.customer_product_code)
                product_display_name = new_value
            line.product_display_name = product_display_name

    product_display_name = fields.Char(
        string="Product display name",
        compute="_compute_product_display_name"
        )

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
            if (line_key in aggregated_move_lines and
                move_line.product_id.default_code and
                move_line.move_id.customer_product_code and
                    move_line.product_id.default_code in name):
                new_value = name.replace(
                    move_line.product_id.default_code,
                    move_line.move_id.customer_product_code)
                name = new_value
                aggregated_move_lines[line_key]['name'] = name
        return aggregated_move_lines
