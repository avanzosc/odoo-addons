# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_cost = fields.Float(
        related="product_id.standard_price",
        digits="Product Price",
        groups="stock.group_stock_manager",
        help=("Standard price of the product " "(product_id.standard_price)."),
    )

    lot_purchase_cost = fields.Float(
        compute="_compute_lot_purchase_cost",
        digits="Product Price",
        groups="stock.group_stock_manager",
        help=(
            "If linked to a lot, takes the lot's purchase cost "
            "(quant.lot_id.purchase_price). Otherwise, uses the "
            "product's standard price "
            "(quant.product_id.standard_price)."
        ),
    )

    lot_purchase_value = fields.Float(
        digits="Account",
        compute="_compute_lot_purchase_value",
        groups="stock.group_stock_manager",
        help=(
            "Quant quantity multiplied by the lot purchase cost "
            "(quant.quantity * quant.lot_purchase_cost)."
        ),
    )

    @api.depends("lot_id", "product_id")
    def _compute_lot_purchase_cost(self):
        for quant in self:
            quant.lot_purchase_cost = (
                quant.lot_id.purchase_price
                if quant.lot_id
                else quant.product_id.standard_price or 0.0
            )

    @api.depends("quantity", "lot_purchase_cost")
    def _compute_lot_purchase_value(self):
        for quant in self:
            quant.lot_purchase_value = quant.quantity * quant.lot_purchase_cost
