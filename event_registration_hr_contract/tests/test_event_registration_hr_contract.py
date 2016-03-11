# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventRegistrationHrContract(common.TransactionCase):

    def setUp(self):
        super(TestEventRegistrationHrContract, self).setUp()
        self.contract_model = self.env['hr.contract']
        self.holiday_model = self.env['calendar.holiday']
        self.account_model = self.env['account.analytic.account']
        self.project_model = self.env['project.project']
        self.sale_model = self.env['sale.order']
        self.event_model = self.env['event.event']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        self.registration_model = self.env['event.registration']
        self.employee = self.env.ref('hr.employee')
        self.hr_holidays_model = self.env['hr.holidays']
        self.employee.address_home_id = self.ref('base.public_partner')
        calendar_line_vals = {
            'date': '2020-03-17',
            'absence_type': self.ref('hr_holidays.holiday_status_comp')}
        calendar_vals = {'name': 'Holidays calendar',
                         'lines': [(0, 0, calendar_line_vals)]}
        self.calendar_holiday = self.holiday_model.create(calendar_vals)
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2020-03-01',
                        'date': '2020-03-31',
                        'festive_calendars':
                        [(6, 0, [self.calendar_holiday.id])]}
        self.account = self.account_model.create(account_vals)
        project_vals = {'name': 'project 1',
                        'analytic_account_id': self.account.id}
        self.project = self.project_model.create(project_vals)
        service_product = self.env.ref('product.product_product_consultant')
        service_product.write({'performance': 5.0,
                               'recurring_service': True})
        service_product.performance = 5.0
        service_product.route_ids = [
            (6, 0,
             [self.ref('procurement_service_project.route_serv_project')])]
        sale_vals = {
            'name': 'sale order 1',
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'project_id': self.account.id,
            'project_by_task': 'no'}
        sale_line_vals = {
            'product_id': service_product.id,
            'name': service_product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': service_product.list_price,
            'performance': 5.0,
            'march': True,
            'week4': True,
            'tuesday': True}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)
        contract_vals = {'name': 'Contract 1',
                         'employee_id': self.employee.id,
                         'partner': self.ref('base.public_partner'),
                         'type_id':
                         self.ref('hr_contract.hr_contract_type_emp'),
                         'wage': 500,
                         'date_start': '2020-02-01'}
        self.contract = self.contract_model.create(contract_vals)
        wiz_vals = {'year': 2020}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context(
            {'active_id':
             self.contract.id}).button_calculate_workables_and_festives()

    def test_event_registration_hr_contract(self):
        self.sale_order.action_button_confirm()
        cond = [('project_id', '=', self.project.id)]
        event = self.event_model.search(cond, limit=1)
        registration_vals = {'event_id': event.id,
                             'partner_id': self.ref('base.public_partner'),
                             'contract': self.contract.id}
        registration = self.registration_model.create(registration_vals)
        registration.with_context(
            {'event_id': event.id}).registration_open()
        registration.button_reg_cancel()
        holiday_vals = {
            'name': 'Administrator',
            'holiday_type': 'employee',
            'holiday_status_id': self.ref('hr_holidays.holiday_status_sl'),
            'employee_id': self.employee.id,
            'date_from': '2020-03-15 00:00:00',
            'date_to': '2020-03-20 00:00:00',
            'type': 'remove'}
        self.holidays = self.hr_holidays_model.create(holiday_vals)
        self.holidays.signal_workflow('confirm')
        self.holidays.signal_workflow('validate')
        self.holidays.signal_workflow('refuse')
