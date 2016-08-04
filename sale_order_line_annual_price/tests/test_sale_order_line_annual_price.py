# -*- coding: utf-8 -*-
# (c) 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderLineAnnualPrice(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineAnnualPrice, self).setUp()
        self.sale_model = self.env['sale.order']
        self.account_model = self.env['account.analytic.account']
        self.project_model = self.env['project.project']
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2025-01-15',
                        'date': '2025-02-28'}
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
            'project_id': self.account.id}
        sale_line_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'product_id': service_product.id,
            'name': service_product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': service_product.list_price,
            'performance': 5.0,
            'january': True,
            'february': True,
            'march': True,
            'may': True,
            'june': True,
            'july': True,
            'august': True,
            'september': True,
            'october': True,
            'november': True,
            'december': True,
            'week1': True,
            'week2': True,
            'week3': True,
            'week4': True,
            'week5': True,
            'week6': True,
            'monday': True,
            'tuesday': True,
            'wednesday': True,
            'thursday': True,
            'friday': True,
            'saturday': True,
            'sunday': True}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_line_annaul_price(self):
        self.sale_order.order_line[0]._compute_line_quotes()
        self.assertNotEqual(
            self.sale_order.order_line[0].monthly_quota, 0,
            'Quotes no generated')
