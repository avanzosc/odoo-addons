# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    purchase_ids = fields.Many2many(
        comodel_name='purchase.order', relation='purchase_invoice_rel',
        column1='invoice_id', column2='purchase_id', string='Purchases',
        copy=True)
    sale_ids = fields.Many2many(
        comodel_name='sale.order', relation='sale_order_invoice_rel',
        column1='invoice_id', column2='order_id', string='Sales', copy=True)
