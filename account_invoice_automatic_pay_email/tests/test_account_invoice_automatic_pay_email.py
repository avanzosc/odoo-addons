# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestAccountInvoiceAutomaticPayEmail(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceAutomaticPayEmail, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.today = fields.Date.from_string(fields.Date.today())
        self.partner = self.browse_ref('base.res_partner_1')
        self.partner.email = 'automaticpayemail@odoo.com'
        self.payment_term = self.browse_ref(
            'account.account_payment_term_15days')
        invoice_vals = {
            'partner_id': self.partner.id,
            'account_id': self.browse_ref('account.a_pay').id,
            'type': 'out_invoice',
            'payment_term': self.payment_term.id}
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
        self.invoice.signal_workflow('invoice_open')

    def test_account_invoice_auotmatic_pay_email(self):
        res = self.invoice.onchange_payment_term_date_invoice(
            self.payment_term.id, '2017-01-01')
        value = res.get('value')
        self.assertEqual(
            value.get('payment_reminder_date'), '2017-01-16',
            'Bad payment reminder date(1)')
        self.invoice.payment_reminder_date = '2017-01-16'
        self.invoice_model.automatic_pay_email()
        self.assertEqual(
            fields.Date.from_string(self.invoice.payment_reminder_date),
            self.today + relativedelta(days=7),
            'Bad payment reminder date(2)')
