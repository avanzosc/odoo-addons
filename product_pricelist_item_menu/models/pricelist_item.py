from odoo import models, fields, api


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    product_brand_id = fields.Many2one('product.brand', string='Brand',
                                       related="product_id.product_brand_id", store=True)
    category_id = fields.Many2one('product.category', string='Product Category',
                                  related="product_id.categ_id", store=True)
