# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestInvoiceFromRepair(common.TransactionCase):

    def setUp(self):
        super(TestInvoiceFromRepair, self).setUp()
        self.partner = self.env.ref('base.res_partner_9')
        self.partner.customer_payment_mode = (
            self.ref('account_payment.payment_mode_1'))
        self.mrp_repair_model = self.env['mrp.repair']
        self.mrp_repair = self.env.ref('mrp_repair.mrp_repair_rmrp2')
        self.partner.property_payment_term = (
            self.ref('account.account_payment_term_15days'))

    def test_repair_to_invoice(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        res = self.mrp_repair.action_invoice_create(group=False)
        invoice = self.env['account.invoice'].browse(res[self.mrp_repair.id])
        self.assertEqual(
            self.partner.customer_payment_mode, invoice.payment_mode_id)
        self.assertEqual(self.partner.customer_payment_mode.bank_id,
                         invoice.partner_bank_id)
        self.assertEqual(self.partner.property_payment_term,
                         invoice.payment_term)
