# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    move_line_amount = fields.Float(
        string="Amount",
        compute="_compute_move_line_amount",
    )

    def _compute_move_line_amount(self):
        for line in self:
            amount = 0
            if (
                line.move_id
                and line.qty_done
                and (line.move_id.sale_line_id or line.move_id.purchase_line_id)
            ):
                if line.move_id.sale_line_id:
                    amount = line.qty_done * line.move_id.sale_line_id.price_unit
                if line.move_id.purchase_line_id:
                    amount = line.qty_done * line.move_id.purchase_line_id.price_unit
            line.move_line_amount = amount

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        picking_lines = self
        if not result or len(self) != len(picking_lines):
            return result
        for clave in result.keys():
            for move_line in self.filtered(
                lambda x: x.move_id and x.qty_done and x.move_id.sale_line_id
            ):
                line_key = self._generate_key_to_found()
                if line_key == clave:
                    price_unit = 0
                    if move_line.move_id.sale_line_id:
                        price_unit = move_line.move_id.sale_line_id.price_unit
                    if move_line.move_id.purchase_line_id:
                        price_unit = move_line.move_id.purchae_line_id.price_unit
                    result[line_key]["price_unit"] = price_unit
                    result[line_key]["move_line_amount"] = (
                        move_line.qty_done * price_unit
                    )
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
