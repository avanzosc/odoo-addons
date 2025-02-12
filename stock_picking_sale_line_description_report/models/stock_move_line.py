# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        picking_lines = self
        if not result or len(self) != len(picking_lines):
            return result
        for clave in result.keys():
            for move_line in self.filtered(
                lambda x: x.move_id and x.move_id.sale_line_id
            ):
                line_key = move_line._generate_key_to_found()
                if line_key in clave:
                    result[clave]["name"] = move_line.move_id.sale_line_id.name
                    result[clave]["description"] = ""
        return result

    def _generate_key_to_found(self):
        uom = self.product_uom_id
        name = self.product_id.display_name
        description = self.move_id.description_picking
        product = self.product_id
        if description == name or description == self.product_id.name:
            description = False
        line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}'
        return line_key
