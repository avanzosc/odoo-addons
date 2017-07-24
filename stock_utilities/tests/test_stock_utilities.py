# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockUtilities(common.TransactionCase):

    def setUp(self):
        super(TestStockUtilities, self).setUp()
        self.orderpoint_model = self.env['stock.warehouse.orderpoint']
        self.product = self.env.ref('product.product_product_9')
        self.template = self.product.product_tmpl_id

    def test_count_orderpoints(self):
        tmpl_count = self.orderpoint_model.search_count(
            [('product_id', 'in', self.template._get_products())])
        product_count = self.orderpoint_model.search_count(
            [('product_id', '=', self.product.id)])
        self.assertEqual(self.template.count_orderpoints, tmpl_count)
        self.assertEqual(self.product.count_orderpoints, product_count)
