from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    basket = fields.Boolean(string='Basket', related='product_id.is_basket', store=True)
