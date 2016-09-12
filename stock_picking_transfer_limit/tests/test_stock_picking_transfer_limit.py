# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockPickingTransferLimit(common.TransactionCase):

    def setUp(self):
        super(TestStockPickingTransferLimit, self).setUp()
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.stock_move_model = self.env['stock.move']
        self.partner = self.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_4')
        picking_type = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        self.picking = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': picking_type[:1].id
        })
        self.picking_move = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking.id,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 15,
            'location_id': picking_type[:1].default_location_src_id.id,
            'location_dest_id': (picking_type[:1].default_location_dest_id.id),
        })
        self.picking.action_confirm()
        self.picking.force_assign()

    def test_transfer_detail_default_get(self):
        res = self.env['stock.transfer_details'].with_context(
            active_id=self.picking.id, active_ids=self.picking.ids,
            active_model='stock.picking').default_get([])
        for item in res.get('item_ids', []):
            self.assertEqual(item.get('quantity', 0),
                             item.get('origin_qty', 0),
                             'Origin qty not correctly loaded.')

    def test_onchange_transfer_detail_qty(self):
        transfer = self.env['stock.transfer_details'].with_context(
            active_id=self.picking.id, active_ids=self.picking.ids,
            active_model='stock.picking').create({})
        item = transfer.item_ids[:1]
        item.quantity = item.origin_qty + 10
        result = item.onchange_quantity()
        self.assertTrue(('warning' in result),
                        'No warning raised in onchange.')
        item.quantity = item.origin_qty - 10
        result = item.onchange_quantity()
        self.assertTrue(('warning' not in result),
                        'Warning raised in onchange.')
