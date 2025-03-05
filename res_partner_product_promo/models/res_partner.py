from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    promo_product_id = fields.Many2one('product.product', string="Promo Product")
