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
    sales_count = fields.Float(
        string="Sales Count", related="product_id.sales_count", store=True
    )
    months_with_stock_sales_count = fields.Float(
        string="Months with Stock (Sales Count)",
        compute="_compute_months_with_stock_sales_count",
    )

    def _compute_months_with_stock_sales_count(self):
        for orderpoint in self:
            months_with_stock = 0
            consumed_last_twelve_months = orderpoint.consumed_last_twelve_months
            if consumed_last_twelve_months:
                virtual_available = orderpoint.product_id.virtual_available
                months_with_stock = virtual_available / (
                    consumed_last_twelve_months / 12
                )
            orderpoint.months_with_stock_sales_count = months_with_stock
