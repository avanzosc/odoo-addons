# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventTrackPresenceHrHolidays(common.TransactionCase):

    def setUp(self):
        super(TestEventTrackPresenceHrHolidays, self).setUp()
        self.contract_model = self.env['hr.contract']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        self.holidays_model = self.env['hr.holidays']
        self.employee = self.env.ref('hr.employee')
        self.employee.address_home_id = self.ref('base.public_partner')
        contract_vals = {'name': 'Contract 1',
                         'employee_id': self.employee.id,
                         'partner': self.ref('base.public_partner'),
                         'type_id':
                         self.ref('hr_contract.hr_contract_type_emp'),
                         'wage': 500,
                         'date_start': '2020-02-01'}
        self.contract = self.contract_model.create(contract_vals)
        wiz = self.wiz_model.with_context(
            {'active_id': self.contract.id}).create({'year': 2020})
        wiz.with_context(
            {'active_id':
             self.contract.id}).button_calculate_workables_and_festives()

    def test_event_track_presence_hr_holidays(self):
        holiday_vals = {
            'name': 'Administrator',
            'holiday_type': 'employee',
            'holiday_status_id': self.ref('hr_holidays.holiday_status_sl'),
            'employee_id': self.employee.id,
            'date_from': '2020-03-15 00:00:00',
            'date_to': '2020-03-20 00:00:00',
            'type': 'remove'}
        self.holidays = self.holidays_model.create(holiday_vals)
        self.holidays.signal_workflow('confirm')
        self.holidays.signal_workflow('validate')
        self.holidays.signal_workflow('refuse')
