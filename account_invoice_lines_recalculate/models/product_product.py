from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    discount_percentage = fields.Float()
