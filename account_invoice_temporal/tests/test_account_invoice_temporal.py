# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestAccountInvoiceTemporal(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceTemporal, self).setUp()
        self.invoice = self.env.ref('account.demo_invoice_0')
        self.account = self.env.ref('account.a_expense')
        self.wiz_model = self.env['account.invoice.confirm']
        self.account.temporal = True

    def test_temporal(self):
        with self.assertRaises(exceptions.Warning):
            self.invoice.check_temporal()
        self.account.temporal = False
        self.invoice.check_temporal()
        self.assertNotEqual(self.invoice.state, 'draft')

    def test_validate_invoices(self):
        wiz = self.wiz_model.create({})
        self.account.temporal = True
        with self.assertRaises(exceptions.Warning):
            wiz.with_context({
                'active_ids': [self.invoice.id]}).invoice_confirm()
        self.account.temporal = False
        wiz.with_context({'active_ids': [self.invoice.id]}).invoice_confirm()
        self.assertNotEqual(self.invoice.state, 'draft')
        with self.assertRaises(exceptions.Warning):
            wiz.with_context({
                'active_ids': [self.invoice.id]}).invoice_confirm()

    def test_temporal_invoice(self):
        self.account.temporal = True
        self.assertEqual(self.invoice.is_temporal, True)
