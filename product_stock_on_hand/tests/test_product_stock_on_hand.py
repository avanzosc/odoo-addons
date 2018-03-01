# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestProductStockOnHand(common.TransactionCase):

    def setUp(self):
        super(TestProductStockOnHand, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.product = self.env.ref('product.product_product_3')
        self.stock_on_hand = self.product.stock_on_hand
        self.tmpl_stock_on_hand = self.product.product_tmpl_id.stock_on_hand
        self.partner = self.ref('base.res_partner_2')
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.location = self.picking_type_in.default_location_dest_id
        self.lot = self.env['stock.production.lot'].create(
            {'product_id': self.product.id,
             'name': ' Test Lot'})
        move_in_vals = {
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 20.0,
            'restrict_lot_id': self.lot.id,
            'location_id': self.picking_type_in.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_in.default_location_dest_id.id,
        }
        self.picking_in = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': self.picking_type_in.id,
            'invoice_state': '2binvoiced',
            'move_lines': [(0, 0, move_in_vals)],
        })
        self.picking_in.action_confirm()
        self.picking_in.action_assign()
        self.picking_in.do_transfer()

    def test_stock_on_hand(self):
        self.assertEqual(self.product.stock_on_hand, (self.stock_on_hand + 20))
        self.assertEqual(self.product.product_tmpl_id.stock_on_hand,
                         (self.tmpl_stock_on_hand + 20))
        self.location.stock_on_hand = False
        self.assertEqual(self.product.stock_on_hand, self.stock_on_hand)
        self.assertEqual(self.product.product_tmpl_id.stock_on_hand,
                         self.tmpl_stock_on_hand)
        self.location.stock_on_hand = True
        self.lot.locked = True
        self.assertEqual(self.product.stock_on_hand,
                         (self.stock_on_hand))
        self.assertEqual(self.product.product_tmpl_id.stock_on_hand,
                         (self.tmpl_stock_on_hand))
        self.lot.locked = False
        today = fields.Datetime.from_string(fields.Datetime.now())
        self.lot.life_date = today
        self.assertEqual(self.product.stock_on_hand,
                         (self.stock_on_hand))
        self.assertEqual(self.product.product_tmpl_id.stock_on_hand,
                         (self.tmpl_stock_on_hand))
        self.lot.life_date = today + relativedelta(days=1)
        self.assertEqual(self.product.stock_on_hand, (self.stock_on_hand + 20))
        self.assertEqual(self.product.product_tmpl_id.stock_on_hand,
                         (self.tmpl_stock_on_hand + 20))

    def test_onchange_stock_on_hand(self):
        self.assertTrue(self.location.stock_on_hand)
        self.location.usage = 'customer'
        self.location.onchange_usage()
        self.assertFalse(self.location.stock_on_hand)
        self.location.usage = 'internal'
        self.location.onchange_usage()
        self.assertTrue(self.location.stock_on_hand)
