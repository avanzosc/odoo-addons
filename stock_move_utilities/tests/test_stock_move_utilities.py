# -*- coding: utf-8 -*-
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests.common import TransactionCase


class TestStockMoveUtilities(TransactionCase):

    def setUp(self):
        super(TestStockMoveUtilities, self).setUp()
        self.quant_model = self.env['stock.quant']
        self.stock_move_model = self.env['stock.move']
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.product = self.browse_ref('product.product_product_3')
        self.location = self.ref('stock.location_inventory')
        self.product = self.env['product.product'].create({
            'name': 'test',
            'type': 'product',
            'product_id': self.product.id,
        })

        self.picking_type_outgoing = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)

        self.stock_picking = self.picking_model.create({
            'picking_type_id': self.picking_type_outgoing[:1].id
        })

        self.env['stock.quant'].create({
            'product_id': self.product.id,
            'location_id': self.location,
            'qty': 30.0,
        })

        self.picking_out_move = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.stock_picking.id,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 8,
            'location_id':
                self.picking_type_outgoing[:1].default_location_src_id.id,
            'location_dest_id':
                self.picking_type_outgoing[:1].default_location_dest_id.id,
        })

        self.stock_move = self.stock_move_model.create({
            'name': 'test',
            'product_id': self.product.id,
            'product_uom_qty': 5.0,
            'product_uom': 1,
            'location_id': self.location,
            'location_dest_id': self.location,
            'price_unit': 10.0,
        })

    def test_stock_move_utilities(self):
        self.stock_move.product_id.virtual_available = 50.0
        self.stock_move.reserved = 10.0
        self.stock_move._compute_unreserved()
        for move in self.stock_move:
            self.assertEquals(move.price_subtotal, 50.0)
            self.assertEquals(move.unreserved, 40.0)

        for move_lines in self.stock_picking.move_lines:
            move_lines.price_subtotal = 50.0
        self.stock_picking._compute_price_total()
        for picking in self.stock_picking:
            self.assertEquals(picking.price_total, 100.0)

        self.product.quants_ids.location_id.usage = 'internal'
        self.product.quants_ids.reservation_id = 33
        for quants in self.product.quants_ids:
            quants.qty = 10.0
        self.product._compute_reserved()
        for product in self.product:
            self.assertEquals(product.reserved, 10.0)
