# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestQualityControlFromHrContract(common.TransactionCase):

    def setUp(self):
        super(TestQualityControlFromHrContract, self).setUp()
        self.contract_model = self.env['hr.contract']
        self.inspection_model = self.env['qc.inspection']
        contract_vals = {'name': 'Contract Test',
                         'employee_id': self.ref('base.partner_root'),
                         'wage': 1.0}
        self.contract = self.contract_model.create(contract_vals)

    def test_quality_control_from_hr_contract(self):
        inspection_vals = {'object_id': ('hr.contract,' +
                                         str(self.contract.id))}
        self.inspection = self.inspection_model.create(inspection_vals)
        self.contract.inspections_from_hr_contract()
        self.assertNotEqual(
            self.contract.inspections_count, 0,
            'Contract without inspections')
