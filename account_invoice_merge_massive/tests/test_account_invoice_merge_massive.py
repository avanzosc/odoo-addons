# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestAccountInvoiceMergeMassive(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceMergeMassive, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.wiz_merge_model = self.env['invoice.merge']
        invoice_vals = {
            'partner_id': self.browse_ref('base.res_partner_1').id,
            'account_id': self.browse_ref('account.a_pay').id,
            'type': 'out_invoice'}
        product = self.browse_ref('product.product_product_6')
        account = self.browse_ref('account.analytic_online')
        line_vals = {
            'product_id': product.id,
            'name': product.name,
            'account_analytic_id': account.id,
            'quantity': 1,
            'price_unit': 800}
        invoice_vals['invoice_line'] = [(0, 0, line_vals)]
        self.invoice1 = self.invoice_model.create(invoice_vals)
        self.invoice2 = self.invoice_model.create(invoice_vals)
        invoice_vals = {
            'partner_id': self.browse_ref('base.res_partner_2').id,
            'account_id': self.browse_ref('account.a_pay').id,
            'type': 'out_invoice'}
        line_vals = {
            'product_id': product.id,
            'name': product.name,
            'account_analytic_id': account.id,
            'quantity': 1,
            'price_unit': 800}
        invoice_vals['invoice_line'] = [(0, 0, line_vals)]
        self.invoice3 = self.invoice_model.create(invoice_vals)
        self.invoice4 = self.invoice_model.create(invoice_vals)

    def test_account_invoice_merge_massive(self):
        wiz = self.wiz_merge_model.create({})
        wiz.with_context(
            active_ids=[self.invoice1.id, self.invoice2.id, self.invoice3.id,
                        self.invoice4.id],
            active_model='account.invoice')._dirty_check()
        wiz.with_context(
            active_ids=[self.invoice1.id, self.invoice2.id, self.invoice3.id,
                        self.invoice4.id]).merge_invoices()
        self.assertEqual(
            self.invoice1.state, 'cancel', 'Bad state for invoice 1')
        self.assertEqual(
            self.invoice2.state, 'cancel', 'Bad state for invoice 2')
        self.assertEqual(
            self.invoice3.state, 'cancel', 'Bad state for invoice 3')
        self.assertEqual(
            self.invoice4.state, 'cancel', 'Bad state for invoice 4')
