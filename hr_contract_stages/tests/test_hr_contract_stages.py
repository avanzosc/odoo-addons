# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestHrContractStages(common.TransactionCase):

    def setUp(self):
        super(TestHrContractStages, self).setUp()
        self.hr_contract_obj = self.env['hr.contract']
        self.contract_stage_obj = self.env['hr.contract.stage']

    def test_default_stage_id(self):
        contract = self.hr_contract_obj.create({
            'name': 'Contract Test',
            'employee_id': self.ref('base.partner_root'),
            'wage': 1.0})
        self.assertEqual(contract.contract_stage_id.sequence, 1)
