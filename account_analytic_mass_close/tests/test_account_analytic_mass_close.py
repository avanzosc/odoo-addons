# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields


class TestAccountAnalyticMassClose(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticMassClose, self).setUp()
        self.account_model = self.env['account.analytic.account']
        self.wiz_close_model = self.env['wiz.close.analytic.account.contract']

    def test_account_analytic_mass_close(self):
        account_vals = {
            'name': 'Test 1 account_analytic_mass_close',
            'type': 'contract',
            'date_start': fields.Date.today(),
            'date': fields.Date.today(),
            'state': 'open'}
        account = self.account_model.create(account_vals)
        self.account_model.automatic_close_analytic_accounts_contract()
        self.assertEquals(account.state, 'close',
                          'State of analytic account contract in not CLOSE')
        account_vals = {
            'name': 'Test 2 account_analytic_mass_close',
            'type': 'contract',
            'date_start': fields.Date.today(),
            'date': fields.Date.today(),
            'state': 'open'}
        account2 = self.account_model.create(account_vals)
        wiz = self.wiz_close_model.create({})
        wiz.with_context(
            active_ids=account2.ids).button_close_analytic_accounts_contracts()
        self.assertEquals(account2.state, 'close',
                          'State of analytic account contract in not CLOSE')
