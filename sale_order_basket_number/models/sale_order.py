from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    basket_count = fields.Integer(string='Basket Lines', compute='_compute_basket_counts', store=True)
    other_count = fields.Integer(string='Other Lines', compute='_compute_basket_counts', store=True)
    basket_type = fields.Selection([
        ('closed', 'Closed'),
        ('expanded', 'Expanded'),
        ('open', 'Open'),
    ], string='Basket Type', compute='_compute_basket_type', store=True)

    @api.depends('order_line.basket')
    def _compute_basket_counts(self):
        for order in self:
            order.basket_count = len(order.order_line.filtered(lambda line: line.basket))
            order.other_count = len(order.order_line.filtered(lambda line: not line.basket))

    @api.depends('basket_count', 'other_count')
    def _compute_basket_type(self):
        for order in self:
            if order.basket_count > 0 and order.other_count == 0:
                order.basket_type = 'closed'
            elif order.basket_count > 0 and order.other_count > 0:
                order.basket_type = 'expanded'
            elif order.basket_count == 0 and order.other_count > 0:
                order.basket_type = 'open'
            else:
                order.basket_type = False
