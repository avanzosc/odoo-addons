# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        for clave in result.keys():
            for move_line in self.filtered(
                lambda x: x.move_id and x.qty_done and x.product_packaging_id
            ):
                line_key = self._generate_keys_to_found()
                if line_key in clave:
                    result[clave]["product_packaging"] = move_line.product_packaging_id
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
