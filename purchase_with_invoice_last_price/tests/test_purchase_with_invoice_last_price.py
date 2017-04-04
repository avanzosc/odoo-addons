# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPurchaseWithInvoiceLastPrice(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseWithInvoiceLastPrice, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.product = self.browse_ref('product.product_product_6')
        value = self.invoice_model.onchange_partner_id(
            'in_invoice', self.ref('base.res_partner_13')).get('value')
        account_vals = {
            'partner_id': self.ref('base.res_partner_13'),
            'type': 'in_invoice',
            'account_id': value.get('account_id')}
        invoice_line_vals = {
            'product_id': self.product.id,
            'name': 'invoice line 1',
            'price_unit': 120}
        account_vals['invoice_line'] = [(0, 0, invoice_line_vals)]
        self.invoice1 = self.invoice_model.create(account_vals)
        self.invoice1.signal_workflow('invoice_open')
        account_vals = {
            'partner_id': self.ref('base.res_partner_13'),
            'type': 'in_invoice',
            'account_id': value.get('account_id')}
        invoice_line_vals = {
            'product_id': self.product.id,
            'name': 'invoice line 2',
            'price_unit': 320}
        account_vals['invoice_line'] = [(0, 0, invoice_line_vals)]
        self.invoice2 = self.invoice_model.create(account_vals)
        self.invoice2.signal_workflow('invoice_open')

    def test_purchase_with_invoice_last_price(self):
        self.assertEquals(self.product.last_invoice_purchase_price, 320.0,
                          'Bad last invoice purchase price in product')
