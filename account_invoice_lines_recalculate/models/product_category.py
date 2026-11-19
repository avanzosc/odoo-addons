from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    discounts_exclude = fields.Boolean(
        string="Exclude from global discount and coupons",
    )
