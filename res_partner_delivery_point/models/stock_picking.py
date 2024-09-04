from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_order_id = fields.Many2one(
        "sale.order",
        "Sales Order",
        related="sale_id",
        store=True,
    )
