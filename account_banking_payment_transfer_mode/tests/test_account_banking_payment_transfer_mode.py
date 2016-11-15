# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAccountBankingPaymentTransferMode(common.TransactionCase):

    def setUp(self):
        super(TestAccountBankingPaymentTransferMode, self).setUp()
        self.acc_move_model = self.env['account.move']
        self.acc_move_line_model = self.env['account.move.line']
        acc_model = self.env['account.account']
        journal_model = self.env['account.journal']
        self.payment_mode = self.ref('account_banking_payment_export.'
                                     'payment_mode_2')
        account_vals = {
            'code': 'TRANSF',
            'name': 'Transfer',
            'user_type': self.ref('account.data_account_type_liability'),
            'type': 'other',
            'reconcile': True
            }
        self.transfer_account = acc_model.create(account_vals)
        journal_vals = {
            'name': 'Transfer journal',
            'code': 'TR',
            'type': 'general',
            'company_id': self.ref('base.main_company')
            }
        self.transfer_journal = journal_model.create(journal_vals)
        payment_vals = {
            'name': 'Payment Mode Test',
            'journal': self.ref('account.bank_journal'),
            'bank_id': self.ref('account_payment.partner_bank_1'),
            'company_id': self.ref('base.main_company'),
            'transfer_account_id': self.transfer_account.id,
            'transfer_journal_id': self.transfer_journal.id,
            'transfer_payment_mode': self.payment_mode,
            'type': self.ref('account_banking_payment_export.'
                             'manual_bank_tranfer')
            }
        self.transfer_paymode = self.env['payment.mode'].create(payment_vals)
        payment_order_vals = {
            'mode': self.transfer_paymode.id,
            'date_prefered': 'due'
            }
        payment_order = self.env['payment.order'].create(
            payment_order_vals)
        invoice = self.env.ref('account.demo_invoice_0')
        invoice.signal_workflow('invoice_open')
        wiz = self.env['payment.order.create'].with_context(
            active_model='payment.order', active_id=payment_order.id,
            active_ids=payment_order.ids)
        wiz_id = wiz.create({})
        wiz_id.search_entries()
        entries = []
        for move_line in invoice.move_id.line_id:
            if move_line.credit and not move_line.debit:
                entries.append((6, 0, [move_line.id]))
        wiz_id.entries = entries
        wiz_id.create_payment()
        payment_order.action_open()
        payment_order.action_sent()

    def test_payment_order(self):
        acc_move_domain = [('journal_id', '=', self.transfer_journal.id)]
        acc_move_ids = self.acc_move_model.search(acc_move_domain)
        acc_line_domain = [('account_id', '=', self.transfer_account.id),
                           ('move_id', 'in', acc_move_ids.ids)]
        acc_move_lines = self.acc_move_line_model.search(acc_line_domain)
        for line in acc_move_lines:
            self.assertEqual(line.payment_mode_id.id, self.payment_mode,
                             'Transfer move lines payment mode not correct.')
