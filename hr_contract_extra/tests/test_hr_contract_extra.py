# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestHrContractExtra(common.TransactionCase):

    def setUp(self):
        super(TestHrContractExtra, self).setUp()
        self.compensation_obj = self.env['hr.contract.compensation']
        self.company = self.env.ref('base.main_company')

    def test_default_currency(self):
        compensation = self.compensation_obj.create({
            'payment_type_id': self.ref('hr_contract_extra.payment_type0'),
            'periodicity_id':
                self.ref('hr_contract_extra.payment_periodicity0'),
            'amount': 15000,
        })
        self.assertEqual(
            compensation.currency_id, self.company.currency_id,
            'Currency doesn\'t match')
