# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestStockUtilities(common.TransactionCase):

    def setUp(self):
        super(TestStockUtilities, self).setUp()
        self.orderpoint_model = self.env['stock.warehouse.orderpoint']
        self.product = self.env.ref('product.product_product_9')
        self.template = self.product.product_tmpl_id

    def test_count_orderpoints(self):
        cond = [('product_tmpl_id', '=', self.template.id)]
        products = self.env['product.product'].search(cond)
        tmpl_count = self.orderpoint_model.search_count(
            [('product_id', 'in', products.ids)])
        product_count = self.orderpoint_model.search_count(
            [('product_id', '=', self.product.id)])
        self.assertEqual(self.template.count_orderpoints, tmpl_count)
        self.assertEqual(self.product.count_orderpoints, product_count)
