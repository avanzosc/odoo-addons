# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestSaleOrderCopyVersion(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderCopyVersion, self).setUp()
        self.product = self.browse_ref('product.product_product_consultant')
        self.sale_model = self.env['sale.order']
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 7,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price
            }
        sale_vals = {
            'name': 'SO0001',
            'partner_id': self.ref('base.res_partner_1'),
            'order_line': [(0, 0, sale_line_vals)],
            }
        self.sale = self.sale_model.create(sale_vals)

    def test_sale_order_version(self):
        self.assertEqual(self.sale.name, self.sale.origin_name)
        sale2 = self.sale.copy()
        self.assertEqual(sale2.name, 'SO0001/2')
        self.assertEqual(sale2.origin_name, 'SO0001')
        self.assertEqual(sale2.version_number, 2)
        sale3 = sale2.copy()
        self.assertEqual(sale3.name, 'SO0001/3')
        self.assertEqual(sale3.origin_name, 'SO0001')
        self.assertEqual(sale3.version_number, 3)
        sale4 = self.sale.copy()
        self.assertEqual(sale4.name, 'SO0001/4')
        self.assertEqual(sale4.origin_name, 'SO0001')
        self.assertEqual(sale4.version_number, 4)
