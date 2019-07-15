# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestStockMoveGenerateInitial(common.TransactionCase):

    def setUp(self):
        super(TestStockMoveGenerateInitial, self).setUp()
        self.product_obj = self.env['product.product']
        self.move_obj = self.env['stock.move']
        self.wiz_obj = self.env['wiz.generate.initial.move']
        self.picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'incoming')], limit=1)
        self.picking = self.env['stock.picking'].search(
            [('picking_type_id', '=', self.picking_type.id)], limit=1)
        product_vals = {'name': 'Product-1',
                        'standard_price': 55}
        self.product1 = self.product_obj.create(product_vals)
        product_vals = {'name': 'Product-2',
                        'standard_price': 66}
        self.product2 = self.product_obj.create(product_vals)

    def test_stock_move_generate_initial(self):
        vals = {'name': self.product1.name,
                'product_id': self.product1.id,
                'product_uom': self.product1.uom_id.id,
                'price_unit': self.product1.standard_price,
                'location_id': self.picking_type.default_location_src_id.id,
                'location_dest_id':
                self.picking_type.default_location_dest_id.id}
        self.move_obj.create(vals)
        self.assertEqual(
            self.product1.with_moves, True, 'Product-1 without stock move')
        self.assertEqual(
            self.product2.with_moves, False, 'Product-2 with stock move')
        wiz = self.wiz_obj.with_context(
            active_ids=self.product2.ids).create(
            {'picking_id': self.picking.id})
        wiz.with_context(active_ids=self.product2.ids).default_get(
            ['picking_id', 'stock_picking_type', 'lines'])
        wiz.with_context(active_ids=self.product2.ids).button_generate_moves()
        self.assertEqual(
            self.product2.with_moves, True, 'Product-2 without stock move')
