# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestCalendarHoliday(common.TransactionCase):

    def setUp(self):
        super(TestCalendarHoliday, self).setUp()
        self.holiday_model = self.env['calendar.holiday']
        self.contract_model = self.env['hr.contract']
        self.calendar_model = self.env['res.partner.calendar']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        calendar_line_vals = {
            'date': '2016-01-06',
            'absence_type': self.ref('hr_holidays.holiday_status_comp')}
        calendar_vals = {'name': 'Holidays calendar',
                         'lines': [(0, 0, calendar_line_vals)]}
        self.calendar_holiday = self.holiday_model.create(calendar_vals)
        contract_vals = {'name': 'Contract 1',
                         'employee_id': self.ref('hr.employee'),
                         'partner': self.ref('base.public_partner'),
                         'type_id':
                         self.ref('hr_contract.hr_contract_type_emp'),
                         'wage': 500,
                         'date_start': '2016-01-02',
                         'date_end': '2016-12-30',
                         'holiday_calendars':
                         [(6, 0, [self.calendar_holiday.id])]}
        self.contract = self.contract_model.create(contract_vals)

    def test_calendar_holiday(self):
        self.calendar_holiday.lines[0].write({'date': '2016-01-06'})
        wiz = self.wiz_model.with_context(
            {'active_id': self.contract.id}).create({'year': 2016})
        vals = ['year']
        wiz.with_context(
            {'active_id': self.contract.id}).default_get(vals)
        wiz.with_context(
            {'active_id':
             self.contract.id}).button_calculate_workables_and_festives()
        cond = [('partner', '=', self.ref('base.public_partner')),
                ('year', '=', 2016)]
        calendar = self.calendar_model.search(cond)
        self.assertNotEqual(
            len(calendar), 0, 'Calendar not generated for partner')
        self.contract.write({'partner': self.ref('base.res_partner_1')})
