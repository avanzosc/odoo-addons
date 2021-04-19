
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    max_per_order = fields.Integer(string="Max product per order",
                                   help="Maximum qty of this product that can be sold on each sale order")
    limit_expiration_days = fields.Integer(string="Sales limitation expiration days",
                                           help="Expiration days for website sales limitation")

    def _combination_info_filter(self):
        max_per_product_order = self.product_brand_id.max_per_product_order
        b2b_virtual_available = self.product_variant_id.sudo().b2b_virtual_available
        limited_categories = self.product_brand_id.limited_categories
        if not limited_categories or self.categ_id in limited_categories:
            if max_per_product_order > 0 and max_per_product_order < b2b_virtual_available:
                return self.product_brand_id.max_per_product_order
        return b2b_virtual_available


class ProductBrand(models.Model):
    _inherit = 'product.brand'

    max_per_order = fields.Integer(string="Max brand products per order",
                                   help="Maximum qty of product from this brand that can be sold on each sale order")
    max_per_product_order = fields.Integer(string="Max from each product per order",
                                   help="Maximum qty from each product from this brand that can be sold on each sale order")
    limited_categories = fields.Many2many(string="Limited categories", comodel_name="product.category")
    limit_expiration_days = fields.Integer(string="Sales limitation expiration days",
                                           help="Expiration days for website sales limitation")
    product_category_ids = fields.Many2many(string="Related product categories", comodel_name="product.category",
                                            compute="_compute_related_categories")

    def _compute_related_categories(self):
        for res in self:
            res.product_category_ids = res.product_ids.mapped('categ_id')

