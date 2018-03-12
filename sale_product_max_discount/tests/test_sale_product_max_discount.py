# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestSaleProductMaxDiscount(common.TransactionCase):

    def setUp(self):
        super(TestSaleProductMaxDiscount, self).setUp()
        self.sale_model = self.env['sale.order']
        self.product = self.browse_ref(
            'product.product_product_consultant')
        line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 15
        }
        sale_vals = {
            'name': 'Test sale order',
            'partner_id': self.ref('base.res_partner_1'),
            'order_line': [(0, 0, line_vals)]
        }
        self.sale_order = self.sale_model.create(sale_vals)

    def test_product_max_discount_field(self):
        self.product.min_margin = 10
        self.product.lst_price = 15
        self.product.standard_price = 5
        result = round((((15.0 - 5.0) - (10.0 / 100 * 15.0)) / 15.0 * 100), 2)
        self.assertAlmostEqual(self.product.max_discount, result)
        self.product.min_margin = 10
        self.product.lst_price = 15
        self.product.standard_price = 14
        result = round((((15.0 - 14.0) - (10.0 / 100 * 15.0)) / 15.0 * 100), 2)
        self.assertNotEqual(self.product.max_discount, result)
        self.assertEqual(self.product.max_discount, 0)

    def test_sale_order_exceed_max_discount(self):
        self.product.min_margin = 10
        self.product.lst_price = 15
        self.product.standard_price = 5
        line = self.sale_order.order_line[0]
        line.discount = 60
        self.sale_order.action_button_confirm()
        self.assertEqual(self.sale_order.state, 'validation')
        self.sale_order.signal_workflow('order_validate')
        self.assertEqual(self.sale_order.state, 'manual')

    def test_sale_order_original_workflow(self):
        self.product.min_margin = 10
        self.product.lst_price = 15
        self.product.standard_price = 5
        line = self.sale_order.order_line[0]
        line.discount = 50
        self.sale_order.action_button_confirm()
        self.assertEqual(self.sale_order.state, 'manual')
