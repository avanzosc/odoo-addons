# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAccountAnalyticInvoicing(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticInvoicing, self).setUp()
        self.partner = self.env.ref('base.res_partner_1')
        self.contract = self.env.ref('account.analytic_support_internal')
        self.partner.customer_payment_mode = (
            self.ref('account_payment.payment_mode_1'))
        self.partner.property_payment_term = (
            self.ref('account.account_payment_term_15days'))

    def test_repair_to_invoice(self):
        res = self.contract._recurring_create_invoice()
        invoice = self.env['account.invoice'].browse(res)
        self.assertEqual(
            self.partner.customer_payment_mode, invoice.payment_mode_id)
        self.assertEqual(self.partner.customer_payment_mode.bank_id,
                         invoice.partner_bank_id)
        self.assertEqual(self.partner.property_payment_term,
                         invoice.payment_term)
