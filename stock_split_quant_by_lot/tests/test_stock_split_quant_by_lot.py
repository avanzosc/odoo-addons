# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common
from openerp import exceptions, fields
from dateutil.relativedelta import relativedelta
import base64
import os


class TestStockSplitQuantByLot(common.TransactionCase):

    def setUp(self):
        super(TestStockSplitQuantByLot, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.picking_type_model = self.env['stock.picking.type']
        self.wiz_transfer_model = self.env['stock.transfer_details']
        self.wiz_split_quant_model = self.env['load.quant.lot.lines']
        cond = [('code', '=', 'incoming'),
                ('default_location_src_id.usage', '=', 'supplier'),
                ('warehouse_id', '=', self.ref('stock.stock_warehouse_shop0'))]
        picking_type_in = self.picking_type_model.search(cond)
        supplier = self.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_3')
        move_vals = {
            'product_id': self.product.id,
            'name': 'TEST Movement',
            'product_uom_qty': 100,
            'product_uom': self.product.uom_id.id,
            'location_id': picking_type_in.default_location_src_id.id,
            'location_dest_id': picking_type_in.default_location_dest_id.id,
        }
        picking_vals = {
            'partner_id': supplier,
            'picking_type_id': picking_type_in.id,
            'move_lines': [(0, 0, move_vals)]
        }
        self.picking_id = self.picking_model.create(picking_vals)
        self.picking_id.action_assign()

    def test_wizard_stock_split_quant_onchange(self):
        self.transfer_picking()
        move = self.picking_id.move_lines[:1]
        self.path = os.path.abspath(os.path.dirname(__file__))
        path1 = u'{}/quant_split_by_lot_csv_error_header.csv'.format(self.path)
        file = open(path1, 'r')
        data = base64.encodestring(file.read())
        file.close()
        split_wiz_vals = {
            'by_text': True,
            'by_file': False,
            'delimiter': ';',
            'lot_numbers': 'test_lot1;test_lot2;test_lot3'
        }
        wiz = self.wiz_split_quant_model.with_context(
            active_model='stock.move', active_ids=move.ids, active_id=move.id
            ).create(split_wiz_vals)
        wiz.by_file = True
        wiz.onchange_by_file()
        self.assertFalse(wiz.by_text)
        self.assertFalse(wiz.lot_numbers)
        self.assertEqual(wiz.delimiter, ',')
        wiz.by_text = True
        wiz.file = data
        wiz.onchange_by_text()
        self.assertFalse(wiz.by_file)
        self.assertFalse(wiz.file)
        self.assertEqual(wiz.delimiter, '\n')

    def test_split_quant_by_lot_view_init(self):
        with self.assertRaises(exceptions.Warning):
            self.wiz_split_quant_model.with_context(
                active_model='stock.move',
                active_ids=self.picking_id.move_lines.ids,
                active_id=self.picking_id.move_lines.id).create({})

    def transfer_picking(self):
        wiz_id = self.picking_id.do_enter_transfer_details().get('res_id')
        wizard = self.wiz_transfer_model.browse(wiz_id)
        wizard.do_detailed_transfer()
        move = self.picking_id.move_lines[:1]
        new_date = (fields.Datetime.from_string(fields.Datetime.now()) -
                    relativedelta(days=1))
        move.quant_ids.sudo().write({'in_date': new_date})

    def test_stock_split_quant_by_lot_text(self):
        self.transfer_picking()
        move = self.picking_id.move_lines[:1]
        split_wiz_vals = {
            'by_text': True,
            'by_file': False,
            'delimiter': ',',
            'lot_numbers': 'test_lot1,test_lot2,test_lot3'
        }
        wiz = self.wiz_split_quant_model.with_context(
            active_model='stock.move', active_ids=move.ids, active_id=move.id
            ).create(split_wiz_vals)
        self.assertEqual(len(wiz.origin_quants), 1)
        self.assertEqual(wiz.origin_quants.qty, 100)
        self.assertEqual(wiz.origin_move_id.id, move.id)
        wiz.load_lines()
        self.assertEqual(len(wiz.line_ids), 4)
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_lot1' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_lot2' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_lot3' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: not x.lot_name and x.qty == 97)))
        wiz.action_validate()
        self.assertEqual(len(move.quant_ids), 4)
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_lot1' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_lot2' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_lot3' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: not x.lot_id and x.qty == 97)))
        split_wiz_vals = {
            'by_text': True,
            'by_file': False,
            'delimiter': ',',
            'lot_numbers': 'test_new_lot1'
        }
        wiz = self.wiz_split_quant_model.with_context(
            active_model='stock.move', active_ids=move.ids, active_id=move.id
            ).create(split_wiz_vals)
        self.assertEqual(len(wiz.origin_quants), 4)
        self.assertEqual(sum(wiz.origin_quants.mapped('qty')), 100)
        self.assertEqual(wiz.origin_move_id.id, move.id)
        wiz.load_lines()
        self.assertEqual(len(wiz.line_ids), 5)
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_new_lot1' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_lot1' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_lot2' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'test_lot3' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: not x.lot_name and x.qty == 96)))
        wiz.action_validate()
        self.assertEqual(len(move.quant_ids), 5)
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_new_lot1' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_lot1' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_lot2' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'test_lot3' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: not x.lot_id and x.qty == 96)))

    def test_stock_split_quant_by_file(self):
        self.transfer_picking()
        move = self.picking_id.move_lines[:1]
        self.path = os.path.abspath(os.path.dirname(__file__))
        path1 = u'{}/quant_split_by_lot_csv_error_header.csv'.format(self.path)
        file = open(path1, 'r')
        data = base64.encodestring(file.read())
        file.close()
        split_wiz_vals = {
            'by_text': False,
            'by_file': True,
            'delimiter': ',',
            'lot_numbers': False,
            'file': data
        }
        wiz = self.wiz_split_quant_model.with_context(
            active_model='stock.move', active_ids=move.ids, active_id=move.id
            ).create(split_wiz_vals)
        with self.assertRaises(exceptions.Warning):
            wiz.load_lines()
        path1 = u'{}/quant_split_by_lot_csv_error_extension.pdf'.format(
            self.path)
        file = open(path1, 'r')
        data = base64.encodestring(file.read())
        file.close()
        wiz.file = data
        with self.assertRaises(exceptions.Warning):
            wiz.load_lines()
        path1 = u'{}/quant_split_by_lot_csv_with_qty.csv'.format(self.path)
        file = open(path1, 'r')
        data = base64.encodestring(file.read())
        file.close()
        wiz.file = data
        self.assertEqual(len(wiz.origin_quants), 1)
        self.assertEqual(wiz.origin_quants.qty, 100)
        self.assertEqual(wiz.origin_move_id.id, move.id)
        wiz.load_lines()
        self.assertEqual(len(wiz.line_ids), 4)
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'with_qty_1' and x.qty == 3)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'with_qty_2' and x.qty == 2)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'with_qty_3' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: not x.lot_name and x.qty == 94)))
        wiz.action_validate()
        self.assertEqual(len(move.quant_ids), 4)
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'with_qty_1' and x.qty == 3)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'with_qty_2' and x.qty == 2)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'with_qty_3' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: not x.lot_id and x.qty == 94)))
        path1 = u'{}/quant_split_by_lot_csv_without_qty.csv'.format(self.path)
        file = open(path1, 'r')
        data = base64.encodestring(file.read())
        file.close()
        split_wiz_vals.update({'file': data})
        wiz = self.wiz_split_quant_model.with_context(
            active_model='stock.move', active_ids=move.ids, active_id=move.id
            ).create(split_wiz_vals)
        self.assertEqual(len(wiz.origin_quants), 4)
        self.assertEqual(sum(wiz.origin_quants.mapped('qty')), 100)
        self.assertEqual(wiz.origin_move_id.id, move.id)
        wiz.load_lines()
        self.assertEqual(len(wiz.line_ids), 7)
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'without_qty_1' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'without_qty_2' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'without_qty_3' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'with_qty_1' and x.qty == 3)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'with_qty_2' and x.qty == 2)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: x.lot_name == 'with_qty_3' and x.qty == 1)))
        self.assertTrue(bool(wiz.line_ids.filtered(
            lambda x: not x.lot_name and x.qty == 91)))
        wiz.line_ids.filtered(lambda x: x.lot_name == 'without_qty_1' and
                              x.qty == 1).write({'qty': 4})
        wiz.line_ids.filtered(lambda x: not x.lot_name and x.qty == 91
                              ).write({'qty': 88})
        wiz.action_validate()
        self.assertEqual(len(move.quant_ids), 7)
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'without_qty_1' and x.qty == 4)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'without_qty_2' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'without_qty_3' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'with_qty_1' and x.qty == 3)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'with_qty_2' and x.qty == 2)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: x.lot_id.name == 'with_qty_3' and x.qty == 1)))
        self.assertTrue(bool(move.quant_ids.filtered(
            lambda x: not x.lot_id and x.qty == 88)))
