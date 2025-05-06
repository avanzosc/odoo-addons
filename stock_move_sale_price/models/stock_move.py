# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_price_unit = fields.Float(
        string="Sale Unit Price",
        digits="Product Price",
        related="sale_line_id.price_unit",
        store=True,
    )
    sale_price_subtotal = fields.Float(
        string="Sale Subtotal",
        digits="Product Price",
        compute="_compute_sale_price_subtotal",
        store=True,
    )

    @api.depends("sale_line_id", "sale_line_id.price_unit", "product_uom_qty")
    def _compute_sale_price_subtotal(self):
        for move in self:
            sale_price_subtotal = 0
            if move.sale_line_id:
                sale_price_subtotal = (
                    move.product_uom_qty * move.sale_line_id.price_unit
                )
            move.sale_price_subtotal = sale_price_subtotal
