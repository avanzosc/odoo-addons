# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderLineAttachedCheck(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineAttachedCheck, self).setUp()
        self.sale_model = self.env['sale.order']
        self.task_model = self.env['project.task']
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2016-02-15',
                        'use_tasks': True}
        self.account = self.env['account.analytic.account'].create(
            account_vals)
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

    def test_sale_order_line_attached_check(self):
        self.sale_order.action_button_confirm()
        cond = [('service_project_sale_line', '=',
                 self.sale_order.order_line[0].id)]
        task = self.task_model.search(cond, limit=1)
        self.assertEqual(
            task.attached, True, 'Task without attached')
        task._catch_attached()
