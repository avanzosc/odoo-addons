# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def write(self, values):
        result = super().write(values)
        if "product_qty" in values:
            for line in self:
                if line.saca_line_id and line.saca_line_id.sale_order_line_ids:
                    line.saca_line_id.sale_order_line_ids[0].product_uom_qty = values[
                        "product_qty"
                    ]
        if "price_unit" in values:
            for line in self:
                if line.saca_line_id and line.saca_line_id.sale_order_line_ids:
                    line.saca_line_id.sale_order_line_ids[0].price_unit = values[
                        "price_unit"
                    ]
                if line.saca_line_id and line.saca_line_id.stock_move_ids:
                    for move in line.saca_line_id.stock_move_ids:
                        move.standard_price = values["price_unit"]
                        move.onchange_standard_price()
                if line.saca_line_id and line.saca_line_id.move_line_ids:
                    for move_line in line.saca_line_id.move_line_ids:
                        move_line.standard_price = values["price_unit"]
                        move_line.onchange_standard_price()
        return result
