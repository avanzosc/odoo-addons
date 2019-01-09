# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestStockInventoryLinePrice(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockInventoryLinePrice, cls).setUpClass()
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

    def test_change_price(self):
        self.inventory.prepare_inventory()
        self.assertEqual(
            self.inventory.line_ids[0].theoretical_subtotal,
            self.inventory.line_ids[0].product_qty *
            self.inventory.line_ids[0].theoretical_std_price)
        self.assertEqual(
            self.inventory.line_ids[0].real_subtotal,
            self.inventory.line_ids[0].product_qty *
            self.inventory.line_ids[0].standard_price)
        self.inventory.line_ids[0].product_qty += 10
        self.assertEqual(
            self.inventory.line_ids[0].theoretical_subtotal,
            self.inventory.line_ids[0].product_qty *
            self.inventory.line_ids[0].theoretical_std_price)
        self.assertEqual(
            self.inventory.line_ids[0].real_subtotal,
            self.inventory.line_ids[0].product_qty *
            self.inventory.line_ids[0].standard_price)
