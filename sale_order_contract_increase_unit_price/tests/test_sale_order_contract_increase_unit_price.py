# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestSaleOrderContractIncreaseUnitPrice(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderContractIncreaseUnitPrice, self).setUp()
        self.wiz_model = self.env['wiz.sale.order.line.increase.unit.price']
        self.sale_model = self.env['sale.order']
        self.account_model = self.env['account.analytic.account']
        self.product = self.browse_ref(
            'product.product_product_7')
        self.service_product = self.browse_ref(
            'product.product_product_consultant')
        account_line_vals = {'product_id': self.product.id,
                             'name': self.product.name,
                             'quantity': 1,
                             'uom_id': self.product.uom_id.id,
                             'price_unit': 1000}
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2025-01-15',
                        'date': '2025-02-28',
                        'use_tasks': True,
                        'recurring_invoices': True,
                        'recurring_invoice_line_ids':
                        [(0, 0, account_line_vals)]}
        self.account = self.account_model.create(account_vals)
        sale_vals = {
            'name': 'Test sale order increase unit price, sale order 1',
            'partner_id': self.ref('base.res_partner_1'),
            'project_id': self.account.id,
        }
        sale_line_vals = {
            'product_id': self.service_product.id,
            'name': self.service_product.name,
            'product_uom_qty': 1,
            'product_uom': self.service_product.uom_id.id,
            'price_unit': 1000}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order1 = self.sale_model.create(sale_vals)

    def test_sale_order_contract_increase_unit_price(self):
        wiz_vals = {'increase': 0.000}
        wiz = self.wiz_model.create(wiz_vals)
        with self.assertRaises(exceptions.Warning):
            wiz.with_context(
                {'active_ids': self.sale_order1.ids}).apply_increase()
        wiz.increase = 0.014
        with self.assertRaises(exceptions.Warning):
            wiz.with_context(
                {'active_ids': self.sale_order1.ids}).apply_increase()
        wiz.write({'contract': True})
        wiz.with_context(
            {'active_ids': self.sale_order1.ids}).apply_increase()
        for line in self.sale_order1.project_id.recurring_invoice_line_ids:
            self.assertEqual(
                line.price_unit, 1014, 'Error in sale contract increase')
