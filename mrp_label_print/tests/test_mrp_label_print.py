# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestMrpLabelPrint(common.TransactionCase):

    def setUp(self):
        super(TestMrpLabelPrint, self).setUp()
        try:
            self.production = self.env.ref(
                'mrp_operations_extension.mrp_production_opeext')
        except:
            self.production = self.env.ref('mrp.mrp_production_2')
        self.ul_id = self.env['product.ul'].create(
            {'name': 'Test', 'qty': 10, 'type': 'unit'})

    def produce_production(self):
        if self.production.state == 'done':
            return True
        self.production.action_confirm()
        self.production.action_assign()
        self.production.force_production()
        wiz = self.env['mrp.product.produce'].with_context(
            active_id=self.production.id, active_ids=[self.production.id],
            active_model='mrp.production').create(
            {'product_id': self.production.product_id.id,
             'product_qty': self.production.product_qty,
             'ul_id': self.ul_id.id,
             'ul_qty': self.production.product_qty / 10})
        self.production.action_produce(self.production.id,
                                       self.production.product_qty,
                                       'consume_produce', wiz=wiz)
        self.production.action_production_end()

    def test_reports_data(self):
        self.produce_production()
        self.assertEqual(self.production.state, 'done')
        self.assertTrue(self.production.report_data_ids)

    def test_mrp_label_report_data(self):
        self.produce_production()
        for report in self.production.report_data_ids:
            report.ul_id = self.ul_id
            to_sum = (report.product_qty % self.ul_id.qty) and 1 or 0
            report.ul_qty = int((report.product_qty / self.ul_id.qty)) + to_sum
        for report in self.production.report_data_ids:
            self.assertEqual(report.ul_qty, report.ul_computed_qty)
        res = self.production.print_label_report()
        self.assertEqual(res['type'], 'ir.actions.report.xml')

    def test_mrp_label_report_data_with_warning(self):
        self.produce_production()
        self.production.report_data_ids[:1].ul_qty += 10
        with self.assertRaises(exceptions.Warning):
            self.production.print_label_report()
