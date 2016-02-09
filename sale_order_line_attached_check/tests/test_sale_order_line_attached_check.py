# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderLineAttachedCheck(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineAttachedCheck, self).setUp()
        self.sale_model = self.env['sale.order']
        self.project_model = self.env['project.project']
        self.task_model = self.env['project.task']
        self.procurement_model = self.env['procurement.order']
        self.event_model = self.env['event.event']
        self.wiz_model = self.env['project.task.create.meeting']
        self.event_copy_model = self.env['events.copy']
        account_vals = {'name': 'account procurement service project'}
        self.account = self.env['account.analytic.account'].create(
            account_vals)
        project_vals = {'name': 'project procurement service project',
                        'date_start': '2016-02-15',
                        'date': '2016-04-15',
                        'analytic_account_id': self.account.id}
        self.project = self.project_model.create(project_vals)
        service_product = self.env.ref('product.product_product_consultant')
        service_product.route_ids = [
            (6, 0,
             [self.ref('procurement_service_project.route_serv_project')])]
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'project_id': self.account.id}
        sale_line_vals = {
            'product_id': service_product.id,
            'name': service_product.name,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': service_product.list_price,
            'attached': True}
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

    def test_sale_order_line_attached_check(self):
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
        cond = [('sale_line_id', '=', self.sale_order.order_line[0].id)]
        procurement = self.procurement_model.search(cond)
        self.assertEqual(
            len(procurement), 1,
            'Procurement not generated for product service')
        procurement.run()
        self.assertEqual(
            len(self.project.tasks), 1,
            'Task not generated from procurement')
        cond = [('service_project_sale_line', '=',
                 self.sale_order.order_line[0].id)]
        task = self.task_model.search(cond, limit=1)
        self.assertEqual(
            task.attached, True, 'Task without attached')
