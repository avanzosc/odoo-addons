# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockPickingValuedEditable(common.TransactionCase):

    def setUp(self):
        super(TestStockPickingValuedEditable, self).setUp()
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.picking_type = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        self.partner = self.env.ref('base.res_partner_2')
        self.partner.valued_picking = False
        self.picking_values = {
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type[:1].id,
        }

    def test_partner_valued_false(self):
        picking = self.picking_model.create(self.picking_values)
        self.assertFalse(picking.valued)
        self.partner.valued_picking = True
        picking.onchange_partner_id_valued()
        self.assertTrue(picking.valued)

    def test_partner_valued_true(self):
        self.partner.valued_picking = True
        picking = self.picking_model.create(self.picking_values)
        self.assertTrue(picking.valued)
        self.partner.valued_picking = False
        picking.onchange_partner_id_valued()
        self.assertFalse(picking.valued)
