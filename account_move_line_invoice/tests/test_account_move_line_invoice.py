# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestAccountMoveLineInvoice(common.TransactionCase):

    def setUp(self):
        super(TestAccountMoveLineInvoice, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.voucher_obj = self.env['account.voucher']
        self.partner = self.env['res.partner'].create(
            {'name': 'Partner for TestAccountMoveLineInvoice'})
        self.payment_term = self.browse_ref(
            'account.account_payment_term_15days')
        invoice_vals = {
            'partner_id': self.partner.id,
            'account_id': self.browse_ref('account.a_pay').id,
            'type': 'out_invoice',
            'payment_term': self.payment_term.id}
        product = self.browse_ref('product.product_product_6')
        self.account = self.browse_ref('account.analytic_online')
        line_vals = {
            'product_id': product.id,
            'name': product.name,
            'account_analytic_id': self.account.id,
            'quantity': 1,
            'price_unit': 800}
        invoice_vals['invoice_line'] = [(0, 0, line_vals)]
        self.invoice = self.invoice_model.create(invoice_vals)
        self.invoice.signal_workflow('invoice_open')
        res = self.voucher_obj._make_journal_search('bank')
        journal_id = res and res[0] or False
        journal = self.env['account.journal'].browse(journal_id)
        res = self.env['account.voucher'].basic_onchange_partner(
            self.partner.id, journal.id, 'bank')
        line = self.env['account.move.line'].search(
            [('move_id', '=', self.invoice.move_id.id),
             ('debit', '>', 0)], limit=1)
        line_vals = {'reconcile': True,
                     'amount_unreconciled': line.debit,
                     'amount_original': line.debit,
                     'amount': line.debit,
                     'type': 'cr',
                     'account_id': line.account_id.id,
                     'move_line_id': line.id}
        voucher_vals = {
            'name': 'voucher for test',
            'comment': 'Write-Off',
            'payment_rate_currency_id': 1,
            'pay_now': 'pay_now',
            'pre_line': True,
            'payment_option': 'without_writeoff',
            'partner_id': self.partner.id,
            'journal_id': journal.id,
            'account_id': res['value'].get('account_id'),
            'amount': 50000,
            'type': 'receipt',
            'line_cr_ids': [(0, 0, line_vals)]}
        self.voucher = self.voucher_obj.create(voucher_vals)
        self.invoice2 = self.env['account.invoice'].search(
            [('state', '=', 'open')], limit=1)
        accounting_partner = self.env[
            'res.partner']._find_accounting_partner(
            self.invoice2.partner_id).id
        default_amount = (self.invoice2.type in ('out_refund', 'in_refund') and
                          (-self.invoice2.residual or self.invoice2.residual))
        default_type = (self.invoice2.type in ('out_invoice', 'out_refund') and
                        ('receipt' or 'payment'))
        ttype = default_type or 'bank'
        if ttype in ('payment', 'receipt'):
            ttype = 'bank'
        res = self.voucher_obj._make_journal_search(ttype)
        journal_id = res and res[0] or False
        journal = self.env['account.journal'].browse(journal_id)
        account = (journal.default_credit_account_id or
                   journal.default_debit_account_id)
        voucher_vals = {'journal_id': journal.id,
                        'account_id': account.id}
        self.voucher2 = self.voucher_obj.with_context(
            {'payment_expected_currency': self.invoice2.currency_id.id,
             'default_partner_id': accounting_partner,
             'default_amount': default_amount,
             'default_reference': self.invoice2.name,
             'close_after_process': True,
             'invoice_type': self.invoice2.type,
             'invoice_id': self.invoice2.id,
             'default_type': default_type,
             'type': default_type}).create(voucher_vals)

    def test_account_move_line_invoice_from_invoice(self):
        self.voucher2.with_context(
            {'active_model': 'account.invoice',
             'invoice_id': self.invoice2.id}).button_proforma_voucher()
        for line in self.voucher.move_id.line_id:
            self.assertIn(self.invoice.number, line.name)

    def test_account_move_line_invoice_from_voucher(self):
        self.voucher.signal_workflow('proforma_voucher')
        lines = self.voucher.move_ids.filtered(
            lambda x: self.invoice.number in x.name)
        self.assertEqual(len(self.voucher.move_ids), len(lines))
