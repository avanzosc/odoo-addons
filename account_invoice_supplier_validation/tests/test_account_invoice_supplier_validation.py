# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAccountInvoiceSupplierValidation(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceSupplierValidation, self).setUp()
        self.invoice = self.env.ref('account.invoice_2')
        self.invoice.type = 'out_invoice'
        self.invoice.name = 'Test supplier invoice validation'
        self.in_invoice = self.env.ref('account.demo_invoice_0')
        self.in_invoice.type = 'in_invoice'
        self.in_invoice.name = 'Test supplier invoice validation'

    def test_account_invoice_client_validation(self):
        out_refund = self.invoice.copy({'type': 'out_refund'})
        self.invoice.signal_workflow('invoice_open')
        self.assertEqual(self.invoice.state, 'open')
        out_refund.signal_workflow('invoice_open')
        self.assertEqual(out_refund.state, 'open')

    def test_account_invoice_supplier_validation(self):
        in_refund = self.in_invoice.copy({'type': 'in_refund'})
        self.in_invoice.signal_workflow('invoice_open')
        self.assertEqual(self.in_invoice.state, 'validation')
        in_refund.signal_workflow('invoice_open')
        self.assertEqual(in_refund.state, 'validation')
        self.in_invoice.signal_workflow('invoice_validation')
        self.assertEqual(self.in_invoice.state, 'open')
        in_refund.signal_workflow('invoice_validation')
        self.assertEqual(in_refund.state, 'open')
