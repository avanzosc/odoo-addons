# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestStockQuantExpiry(common.TransactionCase):

    def setUp(self):
        super(TestStockQuantExpiry, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.product = self.env.ref('product.product_product_3')
        self.partner = self.ref('base.res_partner_2')
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.today = fields.Date.today()
        self.lot = self.env['stock.production.lot'].create({
            'name': 'Lot for tests',
            'product_id': self.product.id,
            'mrp_date': (fields.Date.from_string(self.today) -
                         relativedelta(years=1)),
            'life_date': (fields.Date.from_string(self.today) +
                          relativedelta(years=1))
        })
        move_in_vals = {
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 2.0,
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

    def test_stock_quant_lifespan_progress(self):
        quant = self.picking_in.move_lines[:1].quant_ids[:1]
        self.assertEqual(round(quant.lifespan_progress), 50)
        quant.invalidate_cache()
        self.lot.life_date = self.today
        self.assertEqual(round(quant.lifespan_progress), 100)
