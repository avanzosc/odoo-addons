# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestStockOrderpointFilter(common.TransactionCase):

    def setUp(self):
        super(TestStockOrderpointFilter, self).setUp()
        self.wiz_model = self.env['procurement.orderpoint.compute']
        self.product_model = self.env['product.product']
        self.orderpoint_model = self.env['stock.warehouse.orderpoint']

    def test_stock_orderpoint_filter(self):
        wiz = self.wiz_model.create({
            'locations':
                [(6, 0, [self.ref('stock.stock_location_locations')])],
            'categories':
                [(6, 0, [self.ref('product.product_category_7')])],
        })
        wiz.procure_calculation()
        self.product = self.product_model.create({
            'name': 'product template',
            'type': 'product',
        })
        self.orderpoint_model.create({
            'name': 'stock order point filter',
            'product_id': self.product.id,
            'product_min_qty': 50,
            'product_max_qty': 100,
            'qty_multiple': 1,
        })
        wiz2 = self.wiz_model.create({})
        wiz2.procure_calculation()
