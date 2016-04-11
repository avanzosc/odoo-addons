# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    split_purchases = fields.Many2many(
        'purchase.order', string='Split purchases')
    purchase_parts = fields.Integer(
        string='Purchase split how many parts',
        help='Purchase order number to split the purchase order')
    purchase_from_date = fields.Date(
        string='Purchase split from date',
        help='Expected date on which the first purchase order begins')
    purchase_each_month = fields.Integer(
        string='Purchase split each how many month',
        help='Months interval to generate each purchase order')
