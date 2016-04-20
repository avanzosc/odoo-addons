# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHrContractHistory(common.TransactionCase):

    def setUp(self):
        super(TestHrContractHistory, self).setUp()
        self.contract_model = self.env['hr.contract']
        company = self.env.ref('base.main_company')
        company.weekly_hours = 40
        contract_vals = {
            'name': 'employee contract',
            'type_id': self.ref('hr_contract.hr_contract_type_emp'),
            'employee_id': self.ref('hr.employee_han'),
            'date_start': '2016-03-01',
            'wage': 500}
        historical_vals = {
            'type': 'new',
            'date': '2016-03-01',
            'hours': 35,
            'description': 'description'}
        contract_vals['historicals'] = [(0, 0, historical_vals)]
        self.contract = self.contract_model.create(contract_vals)

    def test_event_calendar_holiday(self):
        self.contract.historicals[0]._calculate_hours_percentage()
        self.assertNotEqual(
            self.contract.historicals[0].percentage, 0,
            'Historical without percentage')
