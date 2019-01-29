# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestAccountMoveLineInvoice(common.TransactionCase):

    def setUp(self):
        super(TestAccountMoveLineInvoice, self).setUp()
        self.voucher_obj = self.env['account.voucher']
        self.invoice_model = self.env['account.invoice']
        self.invoice = self.env['account.invoice'].search(
            [('state', '=', 'open')], limit=1)
        accounting_partner = self.env[
            'res.partner']._find_accounting_partner(self.invoice.partner_id).id
        default_amount = (self.invoice.type in ('out_refund', 'in_refund') and
                          (-self.invoice.residual or self.invoice.residual))
        default_type = (self.invoice.type in ('out_invoice', 'out_refund') and
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
        self.voucher = self.voucher_obj.with_context(
            {'payment_expected_currency': self.invoice.currency_id.id,
             'default_partner_id': accounting_partner,
             'default_amount': default_amount,
             'default_reference': self.invoice.name,
             'close_after_process': True,
             'invoice_type': self.invoice.type,
             'invoice_id': self.invoice.id,
             'default_type': default_type,
             'type': default_type}).create(voucher_vals)

    def test_account_move_line_invoice(self):
        self.voucher.with_context(
            {'active_model': 'account.invoice',
             'invoice_id': self.invoice.id}).button_proforma_voucher()
        for line in self.voucher.move_id.line_id:
            self.assertIn(self.invoice.number, line.name)
