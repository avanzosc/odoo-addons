# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.addons.sale_order_create_event.tests.\
    test_sale_order_create_event_assistant import\
    TestSaleOrderCreateEventAssistant
from openerp import fields


class TestEventRegistrationAnalytic(TestSaleOrderCreateEventAssistant):

    def setUp(self):
        super(TestEventRegistrationAnalytic, self).setUp()
        self.del_reg_model = self.env['wiz.event.delete.canceled.registration']
        self.wiz_change_model = self.env['wiz.registration.to.another.event']
        self.holiday_model = self.env['calendar.holiday']
        self.registration_model = self.env['event.registration']
        self.contract_model = self.env['hr.contract']
        self.calendar_model = self.env['res.partner.calendar']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        self.holidays_model = self.env['hr.holidays']
        self.substitution_model = self.env['wiz.event.substitution']
        self.today = fields.Date.from_string(fields.Date.today())
        self.partner.parent_id = self.parent
        self.env['res.partner.bank'].create({
            'state': 'iban',
            'acc_number': 'ES9121000418450200051332',
            'partner_id': self.partner.parent_id.id,
            'mandate_ids': [(0, 0, {'format': 'sepa',
                                    'signature_date': fields.Date.today()})],
        })

    def test_event_track_registration_open_button(self):
        super(TestEventRegistrationAnalytic,
              self).test_event_track_registration_open_button()
        self.assertEquals(
            self.event.count_all_registrations,
            self.event.count_registrations +
            self.event.count_teacher_registrations)
        teachers = self.event.mapped('employee_registration_ids.partner_id')
        domain = [('partner_id', 'in', teachers.ids)]
        self.assertEquals(
            self.event.count_pickings,
            len(self.env['stock.picking'].search(domain)))
        result = self.event.show_teacher_pickings()
        self.assertEqual(
            result['domain'], domain, 'Error in show pickings')
        domain = [('picking_id.partner_id', 'in', teachers.ids)]
        self.assertEquals(
            self.event.count_moves,
            len(self.env['stock.move'].search(domain)))
        result = self.event.show_teacher_moves()
        self.assertEqual(
            result['domain'], domain, 'Error in show pickings')
        self.assertEquals(self.event.count_presences,
                          len(self.event.mapped('track_ids.presences')))
        result = self.event.show_all_registrations()
        domain = [('id', 'in', self.event.registration_ids.ids)]
        self.assertEqual(
            result['domain'], domain, 'Error in show event registration')
        result = self.event.show_teacher_registrations()
        domain = [('id', 'in',
                   self.event.employee_registration_ids.ids)]
        self.assertEqual(
            result['domain'], domain,
            'Error in show event teacher registrations')
        result = self.event.show_presences()
        domain = [('id', 'in', self.event.mapped('track_ids.presences').ids)]
        self.assertEqual(
            result['domain'], domain, 'Error in show event presences')
        self.assertEquals(self.event.count_all_registrations,
                          len(self.event.no_employee_registration_ids) +
                          len(self.event.employee_registration_ids))
        self.assertEquals(self.event.count_registrations,
                          len(self.event.no_employee_registration_ids))
        self.assertEquals(self.event.count_teacher_registrations,
                          len(self.event.employee_registration_ids))
        self.assertEquals(
            self.event.count_registrations +
            self.event.count_teacher_registrations,
            len(self.event.registration_ids))
        self.event.registration_ids.write({'state': 'draft'})
        self.event.registration_ids[1].unlink()
        self.event.sale_order.project_id.recurring_invoices = False
        for registration in self.event.registration_ids.filtered(
                lambda x: x.state == 'draft'):
            result = registration.button_registration_open()
            wiz_id = result.get('res_id')
            add_wiz = self.wiz_add_model.browse(wiz_id)
            if teachers:
                add_wiz.partner = teachers[0].id
            else:
                add_wiz.partner = (
                    self.event.no_employee_registration_ids[0].partner_id.id)
                add_wiz.partner.employee = self.env.ref('hr.employee_al')
            add_wiz.onchange_partner()
            self.assertFalse(add_wiz.create_account)
        new_event = self.event.copy()
        wiz_another_vals = {
            'new_event_id': new_event.id,
        }
        registration = self.event.registration_ids[0]
        change_wiz = self.wiz_change_model.with_context(
            active_ids=[self.event.registration_ids[0].id]).create(
            wiz_another_vals)
        change_wiz.button_change_registration_event()
        self.assertEqual(
            registration.event_id.id, new_event.id,
            'Registration not found in new event')

    def test_event_track_assistant_delete_from_event(self):
        super(TestEventRegistrationAnalytic,
              self).test_event_track_assistant_delete_from_event()
        self.assertTrue(self.event.registration_ids.filtered(
            lambda x: x.state == 'cancel'))
        del_wiz = self.del_reg_model.with_context(
            active_ids=self.event.ids).create({})
        del_wiz.delete_canceled_registration()
        self.assertFalse(self.event.registration_ids.filtered(
            lambda x: x.state == 'cancel'))

    def test_event_registration_analytic_substitution(self):
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
                         'holiday_calendars':
                         [(6, 0, [self.calendar_holiday.id])]}
        self.contract = self.contract_model.create(contract_vals)
        self.env.ref('hr.employee').address_home_id = (
            self.ref('base.public_partner'))
        self.env.ref('hr.employee').address_home_id.parent_id = (
            self.env.ref('base.res_partner_2'))
        self.env.ref('base.public_partner').employee_id = (
            self.ref('hr.employee'))
        self.calendar_holiday.lines[0].write({'date': '2016-01-06'})
        calendar_vals = {'partner': self.ref('base.public_partner'),
                         'year': self.today.year}
        calendar_line_vals = {
            'partner': self.ref('base.public_partner'),
            'date': '{}-01-06'.format(self.today.year),
            'contract': self.contract.id,
            'festive': True}
        calendar_vals['dates'] = [(0, 0, calendar_line_vals)]
        self.calendar_model.create(calendar_vals)
        self.partner = self.env['res.partner'].create({
            'name': 'Partner',
            'parent_id': self.ref('base.public_partner')
        })
        self.user = self.env['res.users'].create({
            'partner_id': self.partner.id,
            'login': 'user',
            'password': 'pass',
        })
        employee_vals = {
            'name': 'Test Employee',
            'user_id': self.user.id,
            'address_home_id': self.partner.id
        }
        employee_vals.update(
            self.env['hr.employee'].onchange_user(
                user_id=employee_vals['user_id'])['value'])
        self.employee = self.env['hr.employee'].create(employee_vals)
        self.partner.employee_id = self.employee.id
        contract_vals = {'name': 'Contract 2',
                         'employee_id': self.employee.id,
                         'partner': self.partner.id,
                         'type_id':
                         self.ref('hr_contract.hr_contract_type_emp'),
                         'wage': 500,
                         'date_start': '2016-01-02',
                         'holiday_calendars':
                         [(6, 0, [self.calendar_holiday.id])]}
        self.contract2 = self.contract_model.create(contract_vals)
        calendar_vals = {'partner': self.partner.id,
                         'year': self.today.year}
        calendar_line_vals = {
            'partner': self.partner.id,
            'date': '{}-01-06'.format(self.today.year),
            'contract': self.contract2.id,
            'festive': True}
        calendar_vals['dates'] = [(0, 0, calendar_line_vals)]
        self.calendar_model.create(calendar_vals)
        event = self.env.ref('event.event_0')
        event.seats_max = 0
        reg_vals = {
            'partner_id': self.ref('base.public_partner'),
            'name': 'aaaaaaa',
            'date_start': event.date_begin,
            'date_end': event.date_end,
            'contract': self.contract.id,
            'employee': self.contract.employee_id.id}
        event.registration_ids = [(0, 0, reg_vals)]
        hr_holidays_vals = {'name': 'Employee holidays',
                            'holiday_type': 'employee',
                            'holiday_status_id':
                            self.ref('hr_holidays.holiday_status_comp'),
                            'employee_id': self.ref('hr.employee'),
                            'date_from': '2016-01-01 00:00:00',
                            'date_to': '2025-01-01 00:00:00',
                            'number_of_days_temp': 1}
        hr_holidays = self.holidays_model.create(hr_holidays_vals)
        wiz_vals = {
            'holiday': hr_holidays.id,
            'lines': [(0, 0, {'confirm_registration': False,
                              'event': event.id,
                              'employee': self.employee.id})]}
        wiz = self.substitution_model.create(wiz_vals)
        wiz._validate_employee_contract_and_registration(wiz.lines[0])
        wiz._validate_employee_calendar(
            self.today.year, self.today.year, self.partner)
        all_seats_available = event.seats_available
        wiz.substitution_employee_from_thread()
        self.assertEqual(
            all_seats_available, event.seats_available,
            'Bad students counter')
