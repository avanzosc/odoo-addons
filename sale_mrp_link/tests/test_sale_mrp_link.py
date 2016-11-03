# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestSaleMrpLink(common.TransactionCase):

    def setUp(self):
        super(TestSaleMrpLink, self).setUp()
        self.product = self.env.ref('product.product_product_4')
        self.product2 = self.env.ref('product.product_product_3')
        self.sale = self.env.ref('sale.sale_order_1')

    def test_add_mrp_production(self):
        sale_line_vals = {
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 7,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price,
            'order_id': self.sale.id,
            }
        sale_line_vals2 = {
            'product_tmpl_id': self.product2.product_tmpl_id.id,
            'product_id': self.product2.id,
            'name': self.product2.name,
            'product_uom_qty': 7,
            'product_uom': self.product2.uom_id.id,
            'price_unit': self.product2.list_price,
            'order_id': self.sale.id,
            }
        sale_line = self.env['sale.order.line'].create(sale_line_vals)
        sale_line2 = self.env['sale.order.line'].create(sale_line_vals2)
        sale_line.action_create_mrp()
        self.assertTrue(sale_line.mrp_production_id)
        self.assertTrue(sale_line2.need_procurement())
        self.assertFalse(sale_line.need_procurement())
        production = sale_line.mrp_production_id
        self.assertEqual(sale_line.product_line_ids, production.product_lines)
        self.assertEqual(sale_line, production.sale_line)
        self.assertEqual(self.sale, production.sale_order)
        production.product_qty = 5
        production.product_lines[0].cost = 50
        self.assertEqual(sale_line.product_uom_qty, production.product_qty)
        self.assertEqual(
            sale_line.price_unit, production.product_lines[0].cost)
        virtual = production.name
        self.sale.action_button_confirm()
        self.assertNotEqual(virtual, production.name)
        self.assertTrue(production.active)

    def test_shortcuts(self):
        res = self.sale.action_show_manufacturing_orders()
        self.assertEqual(res.get('type', False), 'ir.actions.act_window')
