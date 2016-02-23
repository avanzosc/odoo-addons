# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestStockOrderpointFilter(common.TransactionCase):

    def setUp(self):
        super(TestStockOrderpointFilter, self).setUp()
        self.wiz_model = self.env['procurement.orderpoint.compute']
        self.template_model = self.env['product.template']
        self.product_model = self.env['product.product']
        self.orderpoint_model = self.env['stock.warehouse.orderpoint']

    def test_stock_orderpoint_filter(self):
        wiz_vals = {'locations':
                    [(6, 0, [self.ref('stock.stock_location_locations')])],
                    'categories':
                    [(6, 0, [self.ref('product.product_category_7')])]}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.procure_calculation()
        template_vals = {'name': 'product template',
                         'type': 'product'}
        self.template = self.template_model.create(template_vals)
        product_vals = {'product_tmpl_id': self.template.id}
        self.product = self.product_model.create(product_vals)
        orderpoint_vals = {'name': 'stock order point filter',
                           'product_id': self.product.id,
                           'product_min_qty': 50,
                           'product_max_qty': 100,
                           'qty_multiple': 1}
        self.orderpoint_model.create(orderpoint_vals)
        wiz2 = self.wiz_model.create({})
        wiz2.procure_calculation()
