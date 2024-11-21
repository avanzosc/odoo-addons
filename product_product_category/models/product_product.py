from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_category = fields.Many2one(
        "product.category",
        string="Variant Category",
        store=True,
        readonly=False,
        help="Variant Category derived from the template",
    )
