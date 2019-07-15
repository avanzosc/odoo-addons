# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common
from openerp.exceptions import except_orm


class TestAccountUtilities(common.TransactionCase):

    def setUp(self):
        super(TestAccountUtilities, self).setUp()
        self.journal_id = self.env.ref('account.bank_journal')
        self.invoice = self.env.ref('account.invoice_5')

    def test_unpaid_invoice(self):
        self.assertFalse(self.invoice.payment_date)

    def test_paid_invoice(self):
        amount = self.invoice.amount_total if \
            self.invoice.type == 'out_invoice' else \
            (self.invoice.amount_total * -1)
        self.invoice.pay_and_reconcile(
            pay_amount=amount,
            pay_account_id=self.journal_id.default_debit_account_id.id,
            period_id=self.invoice.period_id.id,
            pay_journal_id=self.journal_id.id,
            writeoff_acc_id=self.journal_id.default_debit_account_id.id,
            writeoff_period_id=self.invoice.period_id.id,
            writeoff_journal_id=self.journal_id.id, name='')
        self.assertEqual(self.invoice.payment_date,
                         min(self.invoice.mapped('payment_ids.date')))

    def test_closed_period_move(self):
        move = self.invoice.move_id
        move.journal_id.update_posted = True
        self.assertTrue(move)
        move.button_cancel()
        moves = self.env['account.move'].search(
            [('period_id', '=', move.period_id.id), ('state', '=', 'draft')])
        moves.button_validate()
        close_wiz = self.env['account.period.close'].with_context(
            active_model='account.period', active_id=move.period_id.id,
            active_ids=[move.period_id.id]).create({'sure': 1})
        close_wiz.data_save()
        with self.assertRaises(except_orm):
            move.button_cancel()
