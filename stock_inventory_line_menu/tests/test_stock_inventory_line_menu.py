# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestStockInventoryLineMenu(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockInventoryLineMenu, cls).setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Product to test',
            'standard_price': 7.0,
        })
        cls.stock_move_obj = cls.env['stock.move']
        cls.inventory = cls.env['stock.inventory'].create({
            'name': 'Test Inventory',
            'filter': 'product',
            'product_id': cls.product.id
            })
        cls.quant = cls.env['stock.quant'].create({
            'name': 'Test Quant',
            'location_id': cls.inventory.location_id.id,
            'product_id': cls.product.id,
            'qty': 2,
        })

    def test_inventory_lines_open(self):
        self.inventory.prepare_inventory()
        self.assertEqual(self.inventory.inventory_lines_count, 1)
        action_dict = self.inventory.action_open_inventory_lines()
        self.assertEqual(
            action_dict.get('domain'), "[('inventory_id', '=', %d)]" %
                                       self.inventory.id)
