# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _compute_get_last_invoice_purchase(self):
        for product in self:
            lines = self.env['account.invoice.line'].search(
                [('product_id', '=', product.id),
                 ('invoice_id.type', '=', 'in_invoice'),
                 ('invoice_id.state', 'in', ['open', 'paid'])]).sorted(
                key=lambda l: l.invoice_id.date_invoice)
            invoice = lines[:1].invoice_id
            product.last_invoice_purchase_id = invoice
            product.last_invoice_purchase_price = lines[:1].price_unit
            product.last_invoice_purchase_date = invoice.date_invoice
            product.last_invoice_supplier_id = invoice.partner_id

    last_invoice_purchase_id = fields.Many2one(
        comodel_name='account.invoice', string='Last invoice purchase',
        compute='_compute_get_last_invoice_purchase')
    last_invoice_purchase_price = fields.Float(
        string='Last invoice purchase price',
        compute='_compute_get_last_invoice_purchase')
    last_invoice_purchase_date = fields.Date(
        string='Last invoice purchase date',
        compute='_compute_get_last_invoice_purchase')
    last_invoice_supplier_id = fields.Many2one(
        comodel_name='res.partner', string='Last invoice supplier',
        compute='_compute_get_last_invoice_purchase')
