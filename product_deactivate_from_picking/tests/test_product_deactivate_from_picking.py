# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProductDeactivateFromPicking(common.TransactionCase):

    def setUp(self):
        super(TestProductDeactivateFromPicking, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.picking_type_model = self.env['stock.picking.type']
        self.wiz_model = self.env['stock.return.picking']
        vals = {'name': 'Product for test',
                'unique': True}
        self.product = self.env['product.product'].create(vals)
        cond = [('code', '=', 'incoming')]
        picking_type = self.picking_type_model.search(cond, limit=1)
        move_vals = {'product_id': self.product.id,
                     'name': self.product.name,
                     'product_uom_qty': 15,
                     'product_uom': self.product.uom_id.id,
                     'location_id': self.ref('stock.stock_location_suppliers'),
                     'location_dest_id': self.ref('stock.stock_location_14')}
        picking_vals = {'partner_id': self.ref('base.res_partner_2'),
                        'picking_type_id': picking_type.id,
                        'move_lines': [(0, 0, move_vals)],
                        'invoice_state': 'none'}
        self.picking = self.picking_model.create(picking_vals)
        self.picking.move_lines[0].action_done()

    def test_product_deactivate_from_picking(self):
        self.assertEquals(self.product.qty_available, 15,
                          'Bad product quantity')
        self.assertEquals(len(self.product.message_ids), 1,
                          'Bad message in product')
        cond = [('code', '=', 'outgoing')]
        picking_type = self.picking_type_model.search(cond, limit=1)
        move_vals = {'product_id': self.product.id,
                     'name': self.product.name,
                     'product_uom_qty': 15,
                     'product_uom': self.product.uom_id.id,
                     'location_id': self.ref('stock.stock_location_14'),
                     'location_dest_id': self.ref('stock.stock_location_7'),
                     'picking_type_id': picking_type.id}
        picking_vals = {'partner_id': self.ref('base.res_partner_2'),
                        'picking_type_id': picking_type.id,
                        'move_lines': [(0, 0, move_vals)],
                        'invoice_state': 'none'}
        out_picking = self.picking_model.create(picking_vals)
        out_picking.move_lines[0].action_done()
        self.assertEquals(self.product.qty_available, 0.0,
                          'Bad product quantity(2)')
        self.assertEquals(self.product.active, False,
                          'The product is active')
        self.assertEquals(self.product.product_tmpl_id.active, False,
                          'The product template is active')
        self.assertEquals(len(self.product.message_ids), 2,
                          'Bad message in product(2)')
        vals = self.wiz_model.with_context(
            active_ids=out_picking.ids, active_id=out_picking.id).default_get(
            ['product_return_moves', 'move_dest_exists'])
        wiz_vals = {'move_dest_exists': vals.get('move_dest_exists'),
                    'product_return_moves':
                    [(0, 0, vals.get('product_return_moves')[0])],
                    'invoice_state': 'none'}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context(active_ids=out_picking.ids,
                         active_id=out_picking.id).create_returns()
        cond = [('origin', '=', out_picking.name)]
        in_picking = self.picking_model.search(cond, limit=1)
        in_picking.move_lines[0].action_done()
        self.assertEquals(self.product.qty_available, 15.0,
                          'Bad product quantity(3)')
        self.assertEquals(self.product.active, True,
                          'The product is not active')
        self.assertEquals(self.product.product_tmpl_id.active, True,
                          'The product template is not active')
        self.assertEquals(len(self.product.message_ids), 3,
                          'Bad message in product(3)')
