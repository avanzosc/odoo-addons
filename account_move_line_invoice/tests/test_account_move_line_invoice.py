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

    def test_account_move_line_invoice(self):
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
                     'type': 'cr',
                     'account_id': self.account.id,
                     'amount_original': line.debit,
                     'move_line_id': line.id,
                     'amount': line.debit}
        voucher_vals = {
            'name': 'voucher for test',
            'partner_id': self.partner.id,
            'journal_id': journal.id,
            'account_id': res['value'].get('account_id'),
            'amount': 50000,
            'type': 'receipt',
            'line_cr_ids': [(0, 0, line_vals)]}
        self.voucher = self.env['account.voucher'].create(voucher_vals)
        lines = self.voucher.move_ids.filtered(
            lambda x: self.invoice.number in x.name)
        self.assertEqual(len(self.voucher.move_ids), len(lines))
