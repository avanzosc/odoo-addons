# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestAccountInvoiceManualAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceManualAnalytic, self).setUp()
        self.invoice_model = self.env['account.invoice']
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
        self.invoice = self.invoice_model.create(invoice_vals)

    def test_account_invoice_manual_analytic(self):
        self.invoice.generate_analytic_lines()
        self.assertEqual(
            len(self.invoice.analytic_line_ids), 1, 'Analytic not generated')
        self.invoice.signal_workflow('invoice_open')
        self.assertEqual(
            len(self.invoice.analytic_line_ids), 0,
            'Invoice with manual analytic')
