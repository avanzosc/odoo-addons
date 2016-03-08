# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderCreateEventHour(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderCreateEventHour, self).setUp()
        self.task_model = self.env['project.task']
        self.sale_model = self.env['sale.order']
        self.account_model = self.env['account.analytic.account']
        self.project_model = self.env['project.project']
        self.event_model = self.env['event.event']
        self.task_model = self.env['project.task']
        self.procurement_model = self.env['procurement.order']
        self.wiz_add_model = self.env['wiz.event.append.assistant']
        self.wiz_del_model = self.env['wiz.event.delete.assistant']
        self.contract_model = self.env['hr.contract']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        self.employee = self.env.ref('hr.employee')
        self.employee.address_home_id = self.env.ref('base.res_partner_26').id
        contract_vals = {'name': 'Contract 1',
                         'employee_id': self.employee.id,
                         'partner': self.env.ref('base.res_partner_26').id,
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
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2016-01-15 00:00:00',
                        'start_time': 5.0,
                        'end_time': 10.0,
                        'date': '2016-02-28 00:00:00'}
        self.account = self.account_model.create(account_vals)
        project_vals = {'name': 'project procurement service project',
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
            'january': True,
            'february': True,
            'week4': True,
            'week5': True,
            'tuesday': True,
            'thursday': True}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_create_event_hour(self):
        self.sale_order.action_button_confirm()
        self.project.tasks[0]._calc_num_sessions()
        self.project.tasks[0].show_sessions_from_task()
        self.project.tasks[0].button_recalculate_sessions()
        cond = [('project_id', '=', self.project.id)]
        event = self.event_model.search(cond, limit=1)
        wiz_vals = {'min_event': event.id,
                    'max_event': event.id,
                    'min_from_date': '2016-01-15 00:00:00',
                    'max_to_date': '2016-02-28 00:00:00',
                    'from_date': '2016-01-15 00:00:00',
                    'to_date': '2016-02-28 00:00:00',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz = self.wiz_add_model.with_context(
            {'active_ids': [event.id]}).create(wiz_vals)
        wiz.with_context({'active_ids': [event.id]}).action_append()
        wiz._update_registration_start_date(event.registration_ids[0])
        wiz._update_registration_date_end(event.registration_ids[0])
        wiz.from_date = '2016-05-01'
        wiz.onchange_dates()
        wiz.update({'from_date': '2016-01-20',
                    'to_date': '2016-01-15'})
        wiz.onchange_dates()
        wiz.update({'from_date': '2016-01-01',
                    'min_from_date': '2016-01-15'})
        wiz.onchange_dates()
        wiz.update({'from_date': '2016-05-01',
                    'max_to_date': '2016-02-28'})
        wiz.onchange_dates()
        wiz.update({'to_date': '2016-01-13',
                    'min_from_date': '2016-01-15'})
        wiz.onchange_dates()
        wiz.update({'to_date': '2016-03-01',
                    'max_to_date': '2016-02-28'})
        wiz.onchange_dates()
        wiz_vals = {'min_event': event.id,
                    'max_event': event.id,
                    'min_from_date': '2016-01-15 00:00:00',
                    'max_to_date': '2016-02-28 00:00:00',
                    'from_date': '2016-01-15 00:00:00',
                    'to_date': '2016-02-28 00:00:00',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz.update(wiz_vals)
        wiz.onchange_dates()
        wiz._prepare_track_search_condition(event)
        wiz = self.wiz_del_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids': [event.id]}).onchange_information()
        vals = ['max_event', 'max_to_date', 'min_from_date', 'min_event',
                'past_sessions', 'start_time', 'from_date', 'later_sessions',
                'to_date', 'partner', 'message', 'end_time']
        wiz.with_context(
            {'active_ids': [event.id]}).default_get(vals)
        wiz.from_date = '2016-05-01'
        wiz._dates_control()
        wiz.update({'from_date': '2016-01-20',
                    'to_date': '2016-01-15'})
        wiz._dates_control()
        wiz.update({'from_date': '2016-01-01',
                    'min_from_date': '2016-01-15'})
        wiz._dates_control()
        wiz.update({'min_from_date': '2016-01-15 00:00:00',
                    'max_to_date': '2016-02-20 00:00:00',
                    'from_date': '2016-02-21 00:00:00',
                    'to_date': '2016-02-28 00:00:00'})
        wiz._dates_control()
        wiz.update({'min_from_date': '2016-02-20 00:00:00',
                    'max_to_date': '2016-02-28 00:00:00',
                    'from_date': '2016-01-15 00:00:00',
                    'to_date': '2016-02-10 00:00:00'})
        wiz._dates_control()
        wiz.update({'min_from_date': '2016-01-15 00:00:00',
                    'max_to_date': '2016-02-20 00:00:00',
                    'from_date': '2016-01-15 00:00:00',
                    'to_date': '2016-02-15 00:00:00'})
        wiz._dates_control()
        wiz_vals = {'min_event': event.id,
                    'max_event': event.id,
                    'min_from_date': '2016-01-15 00:00:00',
                    'max_to_date': '2016-02-28 00:00:00',
                    'from_date': '2016-01-15 00:00:00',
                    'to_date': '2016-02-28 00:00:00',
                    'partner': self.env.ref('base.res_partner_26').id}
        wiz.update(wiz_vals)
        wiz.with_context(
            {'active_ids': [event.id]}).action_nodelete_past_and_later()
        wiz.with_context(
            {'active_ids':
             [event.id]})._delete_registrations_between_dates(
            self.project.tasks[0].sessions)
        wiz.with_context(
            {'active_ids': [event.id]}).action_delete_past_and_later()
        event.registration_ids[0].with_context(
            {'event_id': event.id}).registration_open()
        event.registration_ids[0].button_reg_cancel()
        self.assertNotEqual(
            len(self.project.tasks[0].sessions), 0,
            'Sessions no generated')
