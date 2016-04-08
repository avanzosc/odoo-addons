# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    service_order_line = fields.One2many(
        comodel_name='sale.order.line', inverse_name='order_id',
        domain=[('product_type', '=', 'service')],
        string='SERVICE order lines')
    no_service_order_line = fields.One2many(
        comodel_name='sale.order.line', inverse_name='order_id',
        domain=[('product_type', '!=', 'service')],
        string='NO SERVICE order lines')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_type = fields.Selection(related='product_id.type', store=True)
