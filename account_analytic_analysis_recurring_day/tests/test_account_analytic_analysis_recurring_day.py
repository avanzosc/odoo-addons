# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
import datetime


class TestAccountAnalyticAnalysisRecurringDay(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticAnalysisRecurringDay, self).setUp()
        self.account_model = self.env['account.analytic.account']
        account1_vals = {'name': 'Recurring Day',
                         'recurring_invoices': True,
                         'recurring_interval': 1,
                         'recurring_rule_type': 'monthly',
                         'recurring_next_date': '2025-01-15',
                         'recurring_first_day': True,
                         'recurring_last_day': False,
                         'recurring_the_day': 0}
        self.account1 = self.account_model.create(account1_vals)
        account2_vals = {'name': 'Recurring Day',
                         'recurring_invoices': True,
                         'recurring_interval': 1,
                         'recurring_rule_type': 'monthly',
                         'recurring_next_date': '2025-01-15',
                         'recurring_first_day': False,
                         'recurring_last_day': True,
                         'recurring_the_day': 0}
        self.account2 = self.account_model.create(account2_vals)
        account3_vals = {'name': 'Recurring Day',
                         'recurring_invoices': True,
                         'recurring_interval': 1,
                         'recurring_rule_type': 'monthly',
                         'recurring_next_date': '2025-01-15',
                         'recurring_first_day': False,
                         'recurring_last_day': False,
                         'recurring_the_day': 17}
        self.account3 = self.account_model.create(account3_vals)

    def test_account_analytic_analytis_recurring_day(self):
        self.account1.onchange_recurring_first_day()
        self.account1.recurring_next_date = '2025-01-15'
        date = datetime.datetime.strptime(
            self.account1.recurring_next_date, '%Y-%m-%d').date()
        self.assertNotEqual(
            date.day, 1, 'Error in date with first day')
        self.account2.onchange_recurring_last_day()
        self.account2.recurring_next_date = '2025-01-15'
        date = datetime.datetime.strptime(
            self.account2.recurring_next_date, '%Y-%m-%d').date()
        self.assertNotIn(
            date.day, [28, 29, 30, 31], 'Error in date with last day')
        self.account3.onchange_recurring_the_day()
        self.account3.recurring_next_date = '2025-01-15'
        date = datetime.datetime.strptime(
            self.account3.recurring_next_date, '%Y-%m-%d').date()
        self.assertNotEqual(
            date.day, 17, 'Error in date with day 17')
