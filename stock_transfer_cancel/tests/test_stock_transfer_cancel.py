# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common
from openerp import exceptions


class TestStockTransferCancel(common.TransactionCase):

    def setUp(self):
        super(TestStockTransferCancel, self).setUp()
        self.location_model = self.env['stock.location']
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        partner = self.env['res.partner'].create({
            'name': 'Partner test'
        })
        customer_location = self.location_model.create({
            'usage': 'supplier',
            'name': 'Default Customer Location'
        })
        internal_location = self.location_model.create({
            'usage': 'internal',
            'name': 'Default Internal Location'
        })
        picking_in_type = self.picking_type_model.create({
            'name': 'Incoming picking type',
            'code': 'incoming',
            'sequence_id': self.ref('stock.seq_type_picking_in'),
            'default_location_dest_id': internal_location.id,
            'default_location_src_id': customer_location.id,
            })
        picking_out_type = self.picking_type_model.create({
            'name': 'Outgoing picking type',
            'code': 'outgoing',
            'sequence_id': self.ref('stock.seq_type_picking_out'),
            'default_location_src_id': internal_location.id,
            'default_location_dest_id': customer_location.id,
            })
        product = self.env['product.product'].create({
            'name': 'Test Transfer Cancel Product',
            'type': 'product'
        })
        move_vals = {
            'name': product.name,
            'product_id': product.id,
            'product_uom': product.uom_id.id,
            'product_uom_qty': 15,
            'location_id': picking_in_type.default_location_src_id.id,
            'location_dest_id': picking_in_type.default_location_dest_id.id,
            }
        self.picking_incoming = self.picking_model.create({
            'partner_id': partner.id,
            'picking_type_id': picking_in_type.id,
            'move_lines': [(0, 0, move_vals)]
        })
        move_vals.update({
            'product_uom_qty': 5,
            'location_id': picking_out_type.default_location_src_id.id,
            'location_dest_id': picking_out_type.default_location_dest_id.id,
            })
        self.picking_out = self.picking_model.create({
            'partner_id': partner.id,
            'picking_type_id': picking_out_type.id,
            'move_lines': [(0, 0, move_vals)]
        })

    def test_picking_transfer_cancelling(self):
        self.picking_incoming.action_confirm()
        self.picking_out.action_confirm()
        self.picking_incoming.action_assign()
        self.assertEqual(self.picking_incoming.state, 'assigned')
        self.picking_incoming.action_done()
        self.assertEqual(self.picking_incoming.state, 'done')
        self.picking_out.action_assign()
        self.assertEqual(self.picking_out.state, 'assigned')
        self.picking_out.action_done()
        self.assertEqual(self.picking_out.state, 'done')
        with self.assertRaises(exceptions.Warning):
            self.picking_incoming.action_cancel()
        self.picking_out.action_cancel()
        self.assertEqual(self.picking_out.state, 'cancel')

    def test_picking_forced_transfer_cancel(self):
        self.picking_out.action_confirm()
        self.picking_out.force_assign()
        self.assertEqual(self.picking_out.state, 'assigned')
        self.picking_out.action_done()
        self.assertEqual(self.picking_out.state, 'done')
        self.assertTrue(
            self.picking_out.mapped('move_lines.quant_ids'
                                    ).filtered(lambda x: x.qty < 0))
        self.picking_out.action_cancel()
        self.assertEqual(self.picking_out.state, 'cancel')
        self.assertFalse(
            self.picking_out.mapped('move_lines.quant_ids'
                                    ).filtered(lambda x: x.qty < 0))
