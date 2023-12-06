# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _compute_product_display_name(self):
        for line in self:
            product_display_name = line.product_id.display_name
            if (
                line.picking_id.picking_type_id.code == "outgoing"
                and line.product_id.default_code
                and line.move_id.customer_product_code
                and line.product_id.default_code in product_display_name
            ):
                new_value = product_display_name.replace(
                    line.product_id.default_code, line.move_id.customer_product_code
                )
                product_display_name = new_value
            line.product_display_name = product_display_name

    product_display_name = fields.Char(
        string="Product display name", compute="_compute_product_display_name"
    )

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        out_picking_lines = self.filtered(lambda x: x.picking_code == "outgoing")
        if not result or len(self) != len(out_picking_lines):
            return result
        for clave in result.keys():
            for move_line in self.filtered(
                lambda x: x.product_id.default_code and x.move_id.customer_product_code
            ):
                line_key = self._generate_key_to_found()
                name = move_line.product_id.display_name
                if line_key == clave and move_line.product_id.default_code in name:
                    new_value = name.replace(
                        move_line.product_id.default_code,
                        move_line.move_id.customer_product_code,
                    )
                    name = new_value
                    result[line_key]["name"] = name
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
