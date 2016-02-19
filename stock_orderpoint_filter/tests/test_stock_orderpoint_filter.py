# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestStockOrderpointFilter(common.TransactionCase):

    def setUp(self):
        super(TestStockOrderpointFilter, self).setUp()
        self.wiz_model = self.env['procurement.orderpoint.compute']

    def test_stock_orderpoint_filter(self):
        wiz_vals = {'locations':
                    [(6, 0, [self.ref('stock.stock_location_locations')])],
                    'categories':
                    [(6, 0, [self.ref('product.product_category_7')])]}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.procure_calculation()
