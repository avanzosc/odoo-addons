# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestEventRegistrationAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestEventRegistrationAnalytic, self).setUp()
        self.project_model = self.env['project.project']
        self.task_model = self.env['project.task']
        self.sale_model = self.env['sale.order']
        self.event_model = self.env['event.event']
        self.procurement_model = self.env['procurement.order']
        self.wiz_add_model = self.env['wiz.event.append.assistant']
        self.event_copy_model = self.env['events.copy']
        self.wiz_model = self.env['project.task.create.meeting']
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2016-01-15',
                        'date': '2016-02-28'}
        self.account = self.env['account.analytic.account'].create(
            account_vals)
        project_vals = {'name': 'project procurement service project',
                        'calculation_type': 'date_begin',
                        'date_start': '2016-01-15',
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
        project_vals = {
            'name': 'project for project events',
            'calculation_type': 'date_begin',
            'date_start': '2016-02-28',
            'tasks': [(0, 0, {'name': 'Tarea 1'}),
                      (0, 0, {'name': 'Tarea 2'})]}
        self.project2 = self.project_model.create(project_vals)
        event_vals = {'name': 'event for project copy',
                      'date_begin': '2016-02-28',
                      'date_end': '2016-03-31'}
        self.event2 = self.event_model.create(event_vals)

    def test_event_registration_analytic(self):
        task = self.project2.tasks[0]
        wiz_vals = {'date': '2016-02-28',
                    'duration': 4.0,
                    'type': self.ref('project_events.meeting_type')}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context({'active_ids': [task.id]}).action_meeting()
        cond = [('name', '=', self.project2.name),
                ('project_id', '=', self.project2.id)]
        event = self.event_model.search(cond, limit=1)
        event.agenda_description()
        wiz.with_context({'active_ids': [task.id]}).action_meeting()
        wiz_vals = {'project_id': self.project2.id,
                    'start_date': '2016-05-01'}
        event_copy = self.event_copy_model.create(wiz_vals)
        event_copy.with_context(
            {'active_ids': [self.event2.id]}).copy_events()
        self.sale_order.action_button_confirm()
        self.sale_order.order_line[0].product_id_change_with_wh(
            self.sale_order.pricelist_id.id,
            self.sale_order.order_line[0].product_id.id,
            partner_id=self.sale_order.partner_id.id)
        self.assertEqual(
            self.project.claim_count, 0, 'Project with claim')
        self.assertEqual(
            self.project.tasks[0].claim_count, 0, 'Task with claim')
        wiz_vals = {'from_date': '2016-01-15',
                    'to_date': '2016-02-28',
                    'partner': self.env.ref('base.res_partner_26').id,
                    'show_create_account': True,
                    'create_account': 'yes'}
        wiz = self.wiz_add_model.create(wiz_vals)
        wiz.with_context({'active_ids': [event.id]}).action_append()
        self.assertNotEqual(
            len(event.registration_ids), 0, 'Registration not found')
        event.registration_ids[0].with_context(
            {'event_id': event.id}).registration_open()
        self.assertNotEqual(
            len(event.registration_ids[0].analytic_account), False,
            'Analytic account not found')
