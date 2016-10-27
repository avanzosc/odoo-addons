# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpSupplierLink(common.TransactionCase):

    def setUp(self):
        super(TestMrpSupplierLink, self).setUp()
        self.mrp_model = self.env['mrp.production']
        self.sale = self.env.ref('sale.sale_order_6')

    def test_profit_and_commercial(self):
        sale_line = self.sale.order_line[0]
        sale_line.action_create_mrp()
        self.assertTrue(sale_line.mrp_production_id)
        mrp = self.mrp_model.browse(sale_line.mrp_production_id.id)
        mrp.product_lines[0].cost = 500
        mrp.product_lines[1].cost = 1200
        mrp.profit_percent = 15
        mrp.commercial_percent = 20
        self.assertEqual(
            mrp.product_lines[0].profit,
            self.sale.order_line[0].product_line_ids[0].profit)
        self.assertEqual(
            mrp.product_lines[0].commercial,
            self.sale.order_line[0].product_line_ids[0].commercial)
        self.assertEqual(
            sum(mrp.mapped('product_lines.profit')),
            sum(self.sale.mapped('order_line.product_line_ids.profit')))
        self.assertEqual(
            sum(mrp.mapped('product_lines.commercial')),
            sum(self.sale.mapped('order_line.product_line_ids.commercial')))
