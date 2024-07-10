# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    purchase_cost = fields.Float(
        string="Purchase Cost",
        compute="_compute_purchase_cost",
    )
    purchase_amount_value = fields.Float(
        string="Purchase Value", compute="_compute_purchase_value"
    )

    def _compute_purchase_cost(self):
        for quant in self:
            if quant.lot_id and quant.lot_id.purchase_cost:
                cost = quant.lot_id.purchase_cost
            else:
                cost = quant.product_id.standard_price
            quant.purchase_cost = cost

    def _compute_purchase_value(self):
        for quant in self:
            quant.purchase_amount_value = quant.purchase_cost * quant.inventory_quantity
