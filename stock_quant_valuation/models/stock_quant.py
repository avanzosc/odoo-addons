# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_cost = fields.Float(
        related="product_id.standard_price",
        digits="Product Price",
        groups="stock.group_stock_manager",
        help=("Standard price of the product."),
    )

    lot_cost = fields.Float(
        related="lot_id.purchase_price",
        digits="Product Price",
        groups="stock.group_stock_manager",
        help=("Unit price of the lot."),
    )

    lot_value = fields.Float(
        compute="_compute_lot_value",
        digits="Account",
        groups="stock.group_stock_manager",
        store=True,
        help=("Quant quantity multiplied by the lot cost."),
    )

    cost_mismatch = fields.Boolean(compute="_compute_cost_mismatch", store=True)

    @api.depends("lot_cost", "quantity")
    def _compute_lot_value(self):
        for quant in self:
            quant.lot_value = quant.lot_cost * quant.quantity

    @api.depends("product_cost", "lot_cost")
    def _compute_cost_mismatch(self):
        for quant in self:
            if quant.product_cost and quant.lot_cost:
                quant.cost_mismatch = (
                    float_compare(
                        quant.product_cost,
                        quant.lot_cost,
                        precision_rounding=quant.product_id.uom_id.rounding,
                    )
                    != 0
                )
