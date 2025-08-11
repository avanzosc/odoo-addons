# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_cost = fields.Float(
        string="Cost",
        related="product_id.standard_price",
        digits="Product Price",
        groups="stock.group_stock_manager",
    )
