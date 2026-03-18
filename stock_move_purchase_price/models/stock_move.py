# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    purchase_price_unit = fields.Float(
        string="Purchase Unit Price",
        digits="Product Price",
        related="purchase_line_id.price_unit",
        store=True,
    )
    purchase_price_subtotal = fields.Float(
        string="Purchase Subtotal",
        digits="Product Price",
        compute="_compute_purchase_price_subtotal",
        store=True,
    )

    @api.depends("purchase_line_id", "purchase_line_id.price_unit", "product_uom_qty")
    def _compute_purchase_price_subtotal(self):
        for move in self:
            purchase_price_subtotal = 0
            if move.purchase_line_id:
                purchase_price_subtotal = (
                    move.product_uom_qty * move.purchase_line_id.price_unit
                )
            move.purchase_price_subtotal = purchase_price_subtotal
