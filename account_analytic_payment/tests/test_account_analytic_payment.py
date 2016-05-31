# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona- AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestAccountAnalyticPayment(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticPayment, self).setUp()
        self.analytic_model = self.env['account.analytic.account']
        self.pay_mode = self.env.ref(
            'account_banking_payment_export.payment_mode_2')
        self.partner = self.env.ref('base.res_partner_2')
        self.partner.customer_payment_mode = self.pay_mode
        analytic_vals = {
            'name': 'Test Contract',
            'partner_id': self.partner.id,
            'recurring_next_date':
                (fields.Date.from_string(fields.Date.today()) -
                 relativedelta(months=1)),
            'state': 'open',
            }
        self.contract = self.analytic_model.create(analytic_vals)

    def test_invoice_payment_mode(self):
        inv_vals = self.analytic_model._prepare_invoice(self.contract)
        self.assertEqual(
            inv_vals.get('payment_mode_id', False),
            self.pay_mode.id, 'Invoice Payment Mode is not correct.')
