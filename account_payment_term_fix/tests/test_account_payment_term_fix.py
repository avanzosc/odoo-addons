# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

from openerp import fields
from openerp.tests import common

date2str = fields.Date.to_string
str2date = fields.Date.from_string


class TestAccountPaymentTermFix(common.TransactionCase):

    def setUp(self):
        super(TestAccountPaymentTermFix, self).setUp()
        self.payment_day = 25
        self.term = self.env['account.payment.term'].create({
            'name': '60 days from date of invoice day 25',
            'line_ids': [(0, 0, {'value': 'balance',
                                 'days': 60,
                                 'days2': self.payment_day})],
        })

    def get_due_date(self, date):
        pterm_list = self.term.compute(100, date_ref=date2str(date))[0]
        date_due = max(line[0] for line in pterm_list)
        return str2date(date_due)

    def test_account_payment_term_fixed(self):
        self.term.line_ids[0].write({
            'value': 'fixed',
            'value_amount': 100.0,
        })
        date = datetime(2018, 4, 1)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, date.month + 2)

    def test_account_payment_term_procent(self):
        self.term.line_ids[0].write({
            'value': 'procent',
            'value_amount': 1.0,
        })
        date = datetime(2018, 4, 1)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, date.month + 2)

    def test_account_payment_term_30daymonth(self):
        apr = 4  # April (30 day long)
        date = datetime(2018, apr, 01)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 6)
        date = date.replace(day=25)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 6)
        date = date.replace(day=26)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 6)
        date = date.replace(day=27)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 7)

    def test_account_payment_term_31daymonth(self):
        may = 5  # May (31 day long)
        date = datetime(2018, may, 01)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 7)
        date = date.replace(day=2)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 7)
        date = date.replace(day=25)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 7)
        date = date.replace(day=26)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 7)
        date = date.replace(day=27)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 8)

    def test_account_payment_term_february(self):
        feb = 2  # February (28 day long)
        date = datetime(2018, feb, 01)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 4)
        date = date.replace(day=24)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 4)
        date = date.replace(day=25)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 5)
        date = date.replace(day=26)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 5)

    def test_account_payment_term_leapyear(self):
        feb = 2  # February (29 day long)
        date = datetime(2020, feb, 01)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 4)
        date = date.replace(day=25)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 4)
        date = date.replace(day=26)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 5)
        date = date.replace(day=27)
        date_due = self.get_due_date(date)
        self.assertEqual(date_due.day, self.payment_day)
        self.assertEqual(date_due.month, 5)
