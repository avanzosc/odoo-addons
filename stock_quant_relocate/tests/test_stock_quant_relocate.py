# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests import common


class TestStockQuantRelocate(common.TransactionCase):

    def setUp(self):
        super(TestStockQuantRelocate, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.picking_type_model = self.env['stock.picking.type']
        self.wiz_model = self.env['stock.quant.move']

    def test_stock_quant_relocate(self):
        cond = [('name', '=', 'Receipts'),
                ('warehouse_id', '=', self.ref('stock.stock_warehouse_shop0'))]
        picking_type = self.picking_type_model.search(cond)
        cond = [('state', '=', 'done'),
                ('picking_type_id', '=', picking_type.id)]
        picking = self.picking_model.search(cond, limit=1)
        self.assertEqual(picking.show_relocation_button, False,
                         'Relocation button must be False')
        product = picking.move_lines[0].product_id
        product.default_location = self.ref('stock.location_gate_b')
        res = picking.button_relocate()
        product.categ_id.default_location = self.ref('stock.location_gate_b')
        res = picking.button_relocate()
        context = res.get('context', False)
        self.assertNotEqual(context, False, 'Error in call button_relocate')
        self.assertEqual(context.get('active_model', False), 'stock.quant',
                         'Stock quant not in context active_model')
        self.assertNotEqual(context.get('active_ids', False), False,
                            'active_ids not in context')
        self.assertNotEqual(context.get('active_ids'), [],
                            'active_ids empty in context')
        wiz = self.wiz_model.browse(res.get('res_id'))
        wiz.do_transfer()
        self.assertEqual(picking.relocation_made, True,
                         'Quant no relocated in picking')
