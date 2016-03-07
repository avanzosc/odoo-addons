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
        self.calendar_day_model = self.env['res.partner.calendar.day']
        self.employee = self.env.ref('hr.employee')
        self.employee.address_home_id = self.ref('base.partner_root')
        contract_vals = {'name': 'Contract 1',
                         'employee_id': self.employee.id,
                         'partner': self.ref('base.partner_root'),
                         'type_id':
                         self.ref('hr_contract.hr_contract_type_emp'),
                         'wage': 500,
                         'date_start': '2016-01-02'}
        self.contract = self.contract_model.create(contract_vals)
        wiz = self.wiz_model.with_context(
            {'active_id': self.contract.id}).create({'year': 2016})
        wiz.with_context(
            {'active_id':
             self.contract.id}).button_calculate_workables_and_festives()

    def test_event_track_presence_hr_holidays(self):
        holiday_vals = {
            'name': 'Administrator',
            'holiday_type': 'employee',
            'holiday_status_id': self.ref('hr_holidays.holiday_status_sl'),
            'employee_id': self.employee.id,
            'date_from': '2016-03-15 00:00:00',
            'date_to': '2016-03-20 00:00:00',
            'type': 'remove'}
        self.holidays = self.holidays_model.create(holiday_vals)
        self.holidays.signal_workflow('confirm')
        self.holidays.signal_workflow('validate')
        cond = [('partner', '=', self.ref('base.partner_root')),
                ('date', '>=', '2016-03-15'),
                ('date', '<=', '2016-03-20'),
                ('absence_type', '=',
                 self.ref('hr_holidays.holiday_status_sl'))]
        calendar_days = self.calendar_day_model.search(cond)
        self.assertEqual(
            len(calendar_days), 6, 'Not found in calendar low employee')
        self.holidays.signal_workflow('refuse')
        cond = [('partner', '=', self.ref('base.partner_root')),
                ('date', '>=', '2016-03-15'),
                ('date', '<=', '2016-03-20'),
                ('absence_type', '=', False)]
        calendar_days = self.calendar_day_model.search(cond)
        self.assertEqual(
            len(calendar_days), 6,
            'Not found in calendar without low employee')
