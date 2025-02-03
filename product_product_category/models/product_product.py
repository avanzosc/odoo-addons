from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_category = fields.Many2one(
        "product.category",
        string="Product Category",
        store=True,
        readonly=False,
        help="Product Category derived from the template",
    )
