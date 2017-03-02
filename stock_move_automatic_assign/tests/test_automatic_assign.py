# -*- coding: utf-8 -*-
# (c) Copyright 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.tests.common as common
from datetime import timedelta
from openerp import fields


class TestStockMoveAutomaticAssign(common.TransactionCase):

    def setUp(self):
        super(TestStockMoveAutomaticAssign, self).setUp()
        self.wiz_detail_obj = self.env['stock.transfer_details']
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.stock_move_model = self.env['stock.move']
        self.supplier = self.ref('base.res_partner_2')
        self.customer1 = self.ref('base.res_partner_7')
        self.customer2 = self.ref('base.res_partner_8')
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
        })
        self.picking_type_outgoing = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        self.picking_type_incoming = self.picking_type_model.search(
            [('code', '=', 'incoming')], limit=1)
        self.picking_in = self.picking_model.create({
            'partner_id': self.supplier,
            'picking_type_id': self.picking_type_incoming[:1].id
        })
        self.picking_out1 = self.picking_model.create({
            'partner_id': self.customer1,
            'picking_type_id': self.picking_type_outgoing[:1].id
        })
        self.picking_out2 = self.picking_model.create({
            'partner_id': self.customer2,
            'picking_type_id': self.picking_type_outgoing[:1].id
        })
        today = fields.date.today()
        self.picking_in_move = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking_in.id,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 10,
            'location_id':
                self.picking_type_incoming[:1].default_location_src_id.id,
            'location_dest_id':
                self.picking_type_incoming[:1].default_location_dest_id.id,
        })
        self.picking_out_move1 = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking_out1.id,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 8,
            'location_id':
                self.picking_type_outgoing[:1].default_location_src_id.id,
            'location_dest_id':
                self.picking_type_outgoing[:1].default_location_dest_id.id,
            'date_expected': today + timedelta(days=10)
        })
        self.picking_out_move2 = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking_out2.id,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 10,
            'location_id':
                self.picking_type_outgoing[:1].default_location_src_id.id,
            'location_dest_id':
                self.picking_type_outgoing[:1].default_location_dest_id.id,
            'date_expected': today + timedelta(days=12)
        })
        self.picking_in.action_confirm()
        self.picking_out1.action_confirm()
        self.picking_out2.action_confirm()

    def test_automatic_assign(self):
        for move in self.picking_out1.move_lines:
            self.assertEqual(move.state, 'confirmed',
                             "Move should be confirmed")
        wiz_detail = self.wiz_detail_obj.with_context(
            active_model='stock.picking',
            active_ids=[self.picking_in.id],
            active_id=self.picking_in.id).create(
            {'picking_id': self.picking_in.id})
        wiz_detail.item_ids[0].quantity = 10
        res = wiz_detail.do_detailed_transfer()
        self.assertEquals(self.picking_in.state, 'done')
        for move_in in self.picking_in.move_lines:
            self.assertEquals(move_in.state, 'done')
        for move_out1 in self.picking_out1.move_lines:
            self.assertEqual(move_out1.state, 'assigned',
                             "Move should be assigned")
            self.assertEqual(move_out1.reserved_availability, 8,
                             "All qty reserved")
        for move_out2 in self.picking_out2.move_lines:
            self.assertEqual(move_out2.state, 'confirmed',
                             "Move should be confirmed")
            self.assertEqual(move_out2.reserved_availability, 2,
                             "Partial qty reserved")
        self.assertTrue(self.picking_out1.id in res['res_ids'])
        self.assertTrue(self.picking_out2.id in res['res_ids'])
