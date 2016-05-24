# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockInventoryLineExt(common.TransactionCase):

    def setUp(self):
        super(TestStockInventoryLineExt, self).setUp()
        self.mrp_repair = self.env.ref('mrp_repair.mrp_repair_rmrp1')
        self.inventory_model = self.env['stock.inventory']
        self.product = self.env.ref('product.product_product_11')

    def test_stock_inventory_line(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.assertEqual(self.mrp_repair.state, 'confirmed')
        self.mrp_repair.signal_workflow('repair_ready')
        self.assertEqual(self.mrp_repair.state, 'under_repair')
        inventory_line = {
            'product_id': self.product.id,
            'location_id': self.ref('stock.stock_location_stock'),
            'product_qty': 25.0,
            }
        inventory = self.inventory_model.create({
            'name': 'Test inventory',
            'filter': 'partial',
            'location_id': self.ref('stock.stock_location_stock'),
            'line_ids': [(0, 0, inventory_line)]})
        inventory_line = inventory.line_ids[0]
        self.assertEqual(
            inventory_line.standard_price, self.product.standard_price)
        value = inventory_line.standard_price * inventory_line.product_qty
        self.assertEqual(inventory_line.value, value)
        self.assertEqual(inventory_line.under_repair, 1)
        net_qty = \
            inventory_line.theoretical_qty - inventory_line.under_repair
        self.assertEqual(inventory_line.net_qty, net_qty)
        net_value = inventory_line.net_qty * inventory_line.standard_price
        self.assertEqual(inventory_line.net_value, net_value)
