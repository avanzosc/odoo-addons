from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    manufacturer_id = fields.Many2one(
        "product.manufacturer",
        string="Manufacturer",
        related="product_id.manufacturer_id",
        store=True,
    )
