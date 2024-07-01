from odoo import fields, models 

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_basket = fields.Boolean(string='Is a Basket')
