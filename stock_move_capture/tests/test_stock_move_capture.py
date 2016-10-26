# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestStockMoveCapture(common.TransactionCase):

    def setUp(self):
        super(TestStockMoveCapture, self).setUp()
        self.warehouse = self.env.ref('stock.warehouse0')
        self.wiz = self.env['capture.move'].create({
            'warehouse_id': self.warehouse.id,
            'product_ids': [(0, 0, {
                'product_id': self.ref('product.imac'),
                'quantity': 5,
                'location_id': self.ref('stock.stock_location_stock'),
                'location_dest_id': self.ref('stock.stock_location_customers'),
            })],
        })
        self.pick_model = self.env['stock.picking']

    def test_action_confirm_move(self):
        with self.assertRaises(exceptions.Warning):
            res = self.wiz.action_confirm_move()
        self.warehouse.cap_type_id = self.ref('stock.picking_type_out')
        res = self.wiz.action_confirm_move()
        pick = self.pick_model.browse(res['res_id'])
        self.assertEqual(pick.picking_type_id, self.warehouse.cap_type_id)
        moves = pick.move_lines[0]
        products = self.wiz.product_ids[0]
        self.assertEqual(moves.product_id, products.product_id)
        self.assertEqual(moves.location_id, products.location_id)
        self.assertEqual(moves.location_dest_id, products.location_dest_id)
        self.assertEqual(moves.state, 'done')
        self.assertEqual(pick.state, 'done')
