# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockQuantMergeManualAssign(common.TransactionCase):

    def setUp(self):
        super(TestStockQuantMergeManualAssign, self).setUp()
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.quant_assign_wizard = self.env['assign.manual.quants']
        self.stock_move_model = self.env['stock.move']
        self.partner = self.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_4')
        self.lot = self.env['stock.production.lot'].create({
            'name': 'Test Lot',
            'product_id': self.product.id,
        })
        self.picking_type_in = self.picking_type_model.search(
            [('code', '=', 'incoming')], limit=1)
        self.picking_type_out = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        self.picking_in = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': self.picking_type_in.id
        })
        self.picking_move = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking_in.id,
            'product_id': self.product.id,
            'restrict_lot_id': self.lot.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 25,
            'location_id': self.picking_type_in.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_in.default_location_dest_id.id,
        })
        self.picking_in.action_confirm()
        self.picking_in.action_assign()
        self.picking_in.action_done()
        self.picking_out = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': self.picking_type_out.id
        })
        self.picking_move_out = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking_out.id,
            'product_id': self.product.id,
            'restrict_lot_id': self.lot.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 40,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_out.default_location_dest_id.id,
        })
        self.picking_out.action_confirm()
        self.picking_out.action_assign()

    def test_picking_manual_assign(self):
        self.assertTrue(self.picking_move_out.reserved_quant_ids.id in
                        self.picking_move.quant_ids.ids)
        self.picking_in2 = self.picking_in.copy()
        self.picking_in2.action_confirm()
        self.picking_in2.force_assign()
        self.picking_in2.action_done()
        wizard = self.quant_assign_wizard.with_context(
            active_id=self.picking_move_out.id).create({
                'name': 'New wizard',
            })
        self.assertEqual(len(wizard.quants_lines.ids), 2)
        self.assertEqual(len(wizard.quants_lines.filtered('selected').ids), 1)
        self.assertEqual(wizard.lines_qty, 25.0)
        non_selected_lines = wizard.quants_lines.filtered(lambda x:
                                                          not x.selected)
        self.assertEqual(len(non_selected_lines), 1)
        non_selected_lines[0].selected = True
        non_selected_lines[0].onchange_selected()
        self.assertEqual(wizard.lines_qty, 40.0)
        wizard.assign_quants()
        self.assertEqual(self.picking_move_out.state, 'assigned')
