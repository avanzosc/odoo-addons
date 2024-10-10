from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        related="product_id.consumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        string="Months with stock",
        related="product_id.months_with_stock",
    )
    sales_count = fields.Float(
        string="Sales Count",
        related="product_id.sales_count",
        store=True,
    )
    months_sales_count_and_qty_forecast = fields.Integer(
        string="Months with Stock (Sales Count and Qty Forecast)",
        compute="_compute_months_sales_count_and_qty_forecast",
    )

    # prevision / sales_count * 12
    def _compute_months_sales_count_and_qty_forecast(self):
        for orderpoint in self:
            months_with_stock = 0
            sales_count = orderpoint.sales_count
            if sales_count:
                qty_forecast = orderpoint.qty_forecast
                months_with_stock = round(qty_forecast / (sales_count / 12))
            orderpoint.months_sales_count_and_qty_forecast = months_with_stock
