from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        related="product_id.consumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        string="Months with stock", related="product_id.months_with_stock"
    )
