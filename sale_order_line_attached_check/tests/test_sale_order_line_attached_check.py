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
        self.event_model = self.env['event.event']
        self.event_copy_model = self.env['events.copy']
        account_vals = {'name': 'account procurement service project',
                        'start_date': '2016-02-15'}
        self.account = self.env['account.analytic.account'].create(
            account_vals)
        project_vals = {'name': 'project procurement service project',
                        'date_start': '2016-02-15',
                        'date': '2016-04-15',
                        'analytic_account_id': self.account.id}
        self.project = self.project_model.create(project_vals)
        service_product = self.env.ref('product.product_product_consultant')
        route = self.ref('procurement_service_project.route_serv_project')
        service_product.write(
            {'performance': 5.0,
             'recurring_service': True,
             'route_ids': [(6, 0, [route])]})
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
        project_vals = {
            'name': 'project for project events',
            'calculation_type': 'date_begin',
            'date_start': '2016-02-28',
            'tasks': [(0, 0, {'name': 'Tarea 1'}),
                      (0, 0, {'name': 'Tarea 2'})]}
        self.project3 = self.project_model.create(project_vals)
        event_vals = {'name': 'event for project copy',
                      'date_begin': '2016-02-28',
                      'date_end': '2016-03-31',
                      'project_id': self.project3.id}
        self.event2 = self.event_model.create(event_vals)

    def test_sale_order_line_attached_check(self):
        wiz_vals = {'project_id': self.project2.id,
                    'start_date': '2016-05-01'}
        event_copy = self.event_copy_model.create(wiz_vals)
        event_copy.with_context(
            {'active_ids': [self.event2.id]}).copy_events()
        self.sale_order.action_button_confirm()
        cond = [('service_project_sale_line', '=',
                 self.sale_order.order_line[0].id)]
        task = self.task_model.search(cond, limit=1)
        self.assertEqual(
            task.attached, True, 'Task without attached')
