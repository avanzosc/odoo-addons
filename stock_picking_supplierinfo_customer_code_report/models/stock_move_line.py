# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        out_picking_lines = self.filtered(lambda x: x.picking_code == "outgoing")
        if not result or len(self) != len(out_picking_lines):
            return result
        for clave in result.keys():
            for move_line in self:
                line_key = self._generate_key_to_found()
                product_customer_code = ""
                if move_line.move_id.sale_line_id:
                    product_customer_code = (
                        move_line.move_id.sale_line_id.product_customer_code
                    )
                if line_key == clave:
                    result[line_key]["product_customer_code"] = product_customer_code
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
