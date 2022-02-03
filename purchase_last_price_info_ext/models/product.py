# -*- coding: utf-8 -*-
# © 2022 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_last_purchase(self):
        res = super(ProductProduct, self)._get_last_purchase()
        lines = self.env['purchase.order.line'].search(
            [('product_id', '=', self.id),
             ('state', 'in', ['confirmed', 'done'])]).sorted(
            key=lambda l: l.order_id.date_order, reverse=True)
        self.last_purchase_discount = lines[:1].discount
        self.last_purchase_price_no_discount = lines[:1].price_unit
        self.last_purchase_price =  lines[:1].price_unit * (
            1 -lines[:1].discount * 0.01)
        return res

    last_purchase_discount = fields.Float(
        string='Last Purchase Discount', compute='_get_last_purchase')
    last_purchase_price_no_discount = fields.Float(
        string='Last Purchase Price Without Discount',
        compute='_get_last_purchase')
