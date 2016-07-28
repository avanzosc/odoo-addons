# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestSaleMrpLink(common.TransactionCase):

    def setUp(self):
        super(TestSaleMrpLink, self).setUp()
        self.product = self.env.ref('product.product_product_3')
        self.sale = self.env.ref('sale.sale_order_1')
        self.mrp_production = self.env.ref('mrp.mrp_production_1')

    def test_add_mrp_production(self):
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uos_qty': 7,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price,
            'order_id': self.sale.id,
            'mrp_production_id': [(4, self.mrp_production.id)]
            }
        sale_line = self.env['sale.order.line'].create(sale_line_vals)
        self.assertEqual(
            sale_line.mrp_production_id.id, self.mrp_production.id)
        self.sale.action_button_confirm()
        self.assertTrue(self.mrp_production.show)
        self.assertEqual(self.mrp_production.sale_line, sale_line)
        self.assertEqual(self.mrp_production.sale_order, self.sale)
        self.assertEqual(self.mrp_production.partner, self.sale.partner_id)
        self.assertTrue(self.sale.order_line[0].need_procurement())
        self.assertFalse(sale_line.need_procurement())
