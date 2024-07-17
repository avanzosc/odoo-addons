# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super(StockMoveLine, self)._get_aggregated_product_quantities(**kwargs)
        in_picking_lines = self.filtered(lambda x: x.picking_code == "incoming")
        if not result or len(self) != len(in_picking_lines):
            return result
        for clave in result.keys():
            for move_line in self.filtered(lambda x: x.move_id):
                line_key = self._generate_key_to_found()
                if line_key == clave:
                    result[line_key]["name"] = move_line.move_id.name
        return result

    def _generate_key_to_found(self):
        uom = self.product_uom_id
        name = self.product_id.display_name
        description = self.move_id.description_picking
        product = self.product_id
        if description == name or description == self.product_id.name:
            description = False
        line_key = f'{product.id}_{product.display_name}{description or ""}uom {uom.id}'
        return line_key
