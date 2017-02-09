# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAccountInvoicePartnerBank(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoicePartnerBank, self).setUp()
        self.payment_mode = self.env.ref('account_payment.payment_mode_1')
        self.payment_bank = self.ref('account_payment.partner_bank_1')
        self.partner = self.env.ref('base.res_partner_9')
        self.partner_bank = self.env['res.partner.bank'].create(
            {'partner_id': self.partner.id, 'name': 'Partner Bank',
             'acc_number': '00123456789', 'state': 'bank',
             'bank': self.ref('base.res_bank_1')})
        self.invoice = self.env.ref('account.invoice_2')
        self.in_invoice = self.env.ref('account.demo_invoice_0')
        self.sale = self.env.ref('sale.sale_order_2')
        self.advance_inv_model = self.env['sale.advance.payment.inv']

    def test_payment_mode_bank(self):
        self.payment_mode.partner_bank = False
        self.invoice.payment_mode_id = self.payment_mode
        result = self.invoice.onchange_payment_mode()
        self.assertEqual(self.invoice.partner_bank_id.id, self.payment_bank,
                         'Payment mode bank not correctly loaded.')
        self.assertTrue(result.get('domain', {}).get('partner_bank_id', False),
                        'Onchange does not return a correct domain.')

    def test_payment_mode_partner_bank(self):
        self.payment_mode.partner_bank = True
        self.invoice.payment_mode_id = self.payment_mode
        result = self.invoice.onchange_payment_mode()
        self.assertEqual(self.invoice.partner_bank_id.id, self.partner_bank.id,
                         'Partner bank not correctly loaded.')
        self.assertTrue(result.get('domain', {}).get('partner_bank_id', False),
                        'Onchange does not return a correct domain.')

    def test_payment_mode_in_invoice(self):
        self.payment_mode.partner_bank = False
        self.in_invoice.payment_mode_id = self.payment_mode
        result = self.in_invoice.onchange_payment_mode()
        self.assertFalse(result.get('domain', {}).get('partner_bank_id'),
                         'Onchange does not return a correct domain.')

    def test_payment_from_sale_order(self):
        self.sale.partner_id = self.partner
        self.sale.payment_mode_id = self.payment_mode
        self.payment_mode.partner_bank = True
        self.sale.signal_workflow('order_confirm')
        wiz = self.advance_inv_model.create({
            'advance_payment_method': 'all',
        })
        wiz.with_context({
            'active_model': 'sale.order',
            'active_ids': [self.sale.id],
            'active_id': self.sale.id,
        }).create_invoices()
        self.assertTrue(self.sale.invoice_ids)
        for invoice in self.sale.invoice_ids:
            self.assertEqual(
                invoice.partner_bank_id.id, self.partner_bank.id,
                'Partner bank not correctly loaded.')

    def test_payment_from_sale_order_false(self):
        self.sale.partner_id = self.partner
        self.sale.payment_mode_id = self.payment_mode
        self.payment_mode.partner_bank = False
        self.sale.signal_workflow('order_confirm')
        wiz = self.advance_inv_model.create({'advance_payment_method': 'all'})
        wiz.with_context({
            'active_model': 'sale.order',
            'active_ids': [self.sale.id],
            'active_id': self.sale.id,
        }).create_invoices()
        self.assertTrue(self.sale.invoice_ids)
        for invoice in self.sale.invoice_ids:
            self.assertEqual(
                invoice.partner_bank_id.id, self.payment_bank,
                'Payment mode bank not correctly loaded.')
