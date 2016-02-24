# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderCreateEvent(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderCreateEvent, self).setUp()
        self.task_model = self.env['project.task']
        self.sale_model = self.env['sale.order']
        self.account_model = self.env['account.analytic.account']
        self.project_model = self.env['project.project']
        self.task_model = self.env['project.task']
        self.procurement_model = self.env['procurement.order']
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2016-01-15',
                        'date': '2016-02-28'}
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
        account_vals = {'name': 'account procurement service project 2',
                        'date_start': '2016-01-15',
                        'date': '2016-02-28'}
        self.account2 = self.account_model.create(account_vals)
        project_vals = {'name': 'project procurement service project 2',
                        'analytic_account_id': self.account2.id}
        self.project2 = self.project_model.create(project_vals)
        sale_vals.update({'name': 'sale order 2',
                          'project_id': self.account2.id,
                          'project_by_task': 'yes'})
        self.sale_order2 = self.sale_model.create(sale_vals)

    def test_sale_order_create_event(self):
        self.sale_order.action_button_confirm()
        self.project.tasks[0]._calc_num_sessions()
        self.project.tasks[0].show_sessions_from_task()
        self.project.tasks[0].button_recalculate_sessions()
        self.assertNotEqual(
            len(self.project.tasks[0].sessions), 0,
            'Sessions no generated')

    def test_sale_order_create_event_project_by_task(self):
        self.sale_order2.action_button_confirm()
        cond = [('parent_id', '=', self.account2.id)]
        account = self.account_model.search(cond, limit=1)
        cond = [('analytic_account_id', '=', account.id)]
        project = self.project_model.search(cond, limit=1)
        cond = [('project_id', '=', project.id)]
        task = self.task_model.search(cond, limit=1)
        task._calc_num_sessions()
        task.show_sessions_from_task()
        task.button_recalculate_sessions()
        self.assertNotEqual(
            len(task.sessions), 0,
            'Sessions no generated 2')
