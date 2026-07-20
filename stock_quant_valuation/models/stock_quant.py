# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_cost = fields.Float(
        string="Cost",
        related="product_id.standard_price",
        store=True,
        company_dependent=True,
        min_display_digits="Product Price",
        groups="stock.group_stock_manager",
        help=("Standard price of the product."),
    )
    cost_value = fields.Float(
        compute="_compute_cost_value",
        min_display_digits="Product Price",
        groups="stock.group_stock_manager",
        store=True,
        company_dependent=True,
        help=("Quant quantity multiplied by cost."),
    )
    lot_cost = fields.Float(
        compute="_compute_lot_cost",
        store=True,
        min_display_digits="Product Price",
        groups="stock.group_stock_manager",
        help=("Unit price of the lot if lot, otherwise purchase last price."),
    )

    lot_value = fields.Float(
        compute="_compute_lot_value",
        min_display_digits="Product Price",
        groups="stock.group_stock_manager",
        store=True,
        help=("Quant quantity multiplied by the lot cost."),
    )
    cost_mismatch = fields.Boolean(compute="_compute_cost_mismatch", store=True)

    @api.depends("product_cost", "quantity")
    def _compute_cost_value(self):
        for quant in self:
            quant.cost_value = quant.product_cost * quant.quantity

    @api.depends("lot_cost", "quantity")
    def _compute_lot_value(self):
        for quant in self:
            quant.lot_value = quant.lot_cost * quant.quantity

    @api.depends("lot_id", "product_id")
    def _compute_lot_cost(self):
        for quant in self:
            if quant.lot_id:
                quant.lot_cost = quant.lot_id.purchase_price
            else:
                quant.lot_cost = quant.product_id.last_purchase_price

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

    @api.model
    def recompute_lot_fields(self):
        self._compute_cost_value()
        self._compute_lot_cost()
        self._compute_lot_value()
        self._compute_cost_mismatch()
