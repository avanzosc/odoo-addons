# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestStockPickingLabelPrint(common.TransactionCase):

    def setUp(self):
        super(TestStockPickingLabelPrint, self).setUp()
        self.picking = self.env.ref('stock.incomming_shipment')
        self.wiz_model = self.env['stock.transfer_details']
        self.ul_id = self.env['product.ul'].create(
            {'name': 'Test', 'qty': 10, 'type': 'unit'})

    def picking_transfer(self):
        self.picking.action_confirm()
        self.picking.action_assign()
        self.picking.force_assign()
        transfer = self.wiz_model.with_context(
            active_id=self.picking.id, active_ids=[self.picking.id],
            active_model='stock.picking').create(
                {'picking_id': self.picking.id})
        transfer.with_context(active_id=self.picking.id,
                              active_ids=[self.picking.id],
                              active_model='stock.picking'
                              ).do_detailed_transfer()

    def test_test_picking(self):
        self.picking_transfer()
        self.assertEqual(self.picking.state, 'done')
        self.assertTrue(self.picking.report_data_ids)

    def test_picking_label_report_data(self):
        self.picking_transfer()
        for report in self.picking.report_data_ids:
            report.ul_id = self.ul_id
            to_sum = (report.product_qty % self.ul_id.qty) and 1 or 0
            report.ul_qty = int((report.product_qty / self.ul_id.qty)) + to_sum
        for report in self.picking.report_data_ids:
            self.assertEqual(report.ul_qty, report.ul_computed_qty)
        res = self.picking.print_label_report()
        self.assertEqual(res['type'], 'ir.actions.report.xml')

    def test_picking_label_report_data_with_warning(self):
        self.picking_transfer()
        self.picking.report_data_ids[:1].ul_qty += 1
        with self.assertRaises(exceptions.Warning):
            self.picking.print_label_report()
