# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestStockPickingWarning(common.TransactionCase):

    def setUp(self):
        super(TestStockPickingWarning, self).setUp()
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.move_model = self.env['stock.move']
        self.product = self.env.ref('product.product_product_6')

    def test_stock_picking_warning_warning(self):
        self.product.write(
            {'out_picking_warn': 'warning',
             'out_picking_warn_msg': 'aaa',
             'in_picking_warn': 'warning',
             'in_picking_warn_msg': 'bbb'})
        type = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        res = self.move_model.with_context(
            default_picking_type_id=type.id).onchange_product_id(
            prod_id=self.product.id)
        warning = res.get('warning')
        type = self.picking_type_model.search(
            [('code', '=', 'incoming')], limit=1)
        res = self.move_model.with_context(
            default_picking_type_id=type.id).onchange_product_id(
            prod_id=self.product.id)
        warning = res.get('warning')
        self.assertEqual(warning['message'], u'bbb')

    def test_stock_picking_warning_out_picking_transfer(self):
        cond = [('state', '=', 'assigned'),
                ('picking_type_id.code', '=', 'outgoing')]
        picking = self.picking_model.search(cond, limit=1)
        picking.move_lines[0].product_id.write(
            {'out_picking_warn': 'block',
             'out_picking_warn_msg': 'ccc'})
        with self.assertRaises(exceptions.Warning):
            picking.do_enter_transfer_details()
        picking.move_lines[0].product_id.write(
            {'out_picking_warn': 'no-message'})
        res = picking.do_enter_transfer_details()
        context = res.get('context')
        self.assertEqual(context.get('active_id'), picking.id)

    def test_stock_picking_warning_in_picking_transfer(self):
        cond = [('state', '=', 'assigned'),
                ('picking_type_id.code', '=', 'incoming')]
        picking = self.picking_model.search(cond, limit=1)
        picking.move_lines[0].product_id.write(
            {'in_picking_warn': 'block',
             'in_picking_warn_msg': 'ddd'})
        with self.assertRaises(exceptions.Warning):
            picking.do_enter_transfer_details()
        picking.move_lines[0].product_id.write(
            {'in_picking_warn': 'no-message'})
        res = picking.do_enter_transfer_details()
        context = res.get('context')
        self.assertEqual(context.get('active_id'), picking.id)
