# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


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

    @api.multi
    @api.depends('product_id')
    def _compute_product_type(self):
        for line in self:
            line.product_type = ''
            if line.product_id:
                line.product_type = line.product_id.type

    product_type = fields.Char(
        string='Product type', compute='_compute_product_type', store=True)
