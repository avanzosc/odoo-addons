# -*- coding: utf-8 -*-
# © 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockLabelPrint(common.TransactionCase):

    def setUp(self):
        super(TestStockLabelPrint, self).setUp()
        self.wiz_obj = self.env['stock.print.label']
        self.picking = self.env.ref('stock.incomming_shipment')
        self.picking.action_confirm()
        self.picking.action_assign()
        self.picking.force_assign()
        self.picking.action_done()
        self.production = self.env.ref('mrp.mrp_production_2')
        self.production.action_confirm()
        self.production.action_assign()
        self.production.force_production()
        self.production.action_produce(self.production.id,
                                       self.production.product_qty,
                                       'consume_produce')
        self.production.action_production_end()
        self.ul_id = self.env['product.ul'].create({'name': 'Test',
                                                    'qty': 10,
                                                    'type': 'unit'})

    def test_default_get_from_picking(self):
        wiz = self.wiz_obj.with_context(active_model='stock.picking',
                                        active_id=self.picking.id,
                                        active_ids=[self.picking.id]
                                        ).create({})
        moves = self.picking.move_lines.filtered(lambda x: x.state == 'done')
        self.assertEqual(len(moves.mapped('quant_ids')),
                         len(wiz.print_label_lines))

    def test_default_get_from_production(self):
        wiz = self.wiz_obj.with_context(active_model='mrp.production',
                                        active_id=self.production.id,
                                        active_ids=[self.production.id]
                                        ).create({})
        moves = self.production.move_created_ids2.filtered(
            lambda x: x.state == 'done')
        self.assertEqual(len(moves.mapped('quant_ids')),
                         len(wiz.print_label_lines))

    def test_print_label(self):
        wiz = self.wiz_obj.with_context(active_model='stock.picking',
                                        active_id=self.picking.id,
                                        active_ids=[self.picking.id]
                                        ).create({})
        self.assertEqual(wiz.print_label().get('type'),
                         'ir.actions.report.xml')

    def test_onchange_ul(self):
        wiz = self.wiz_obj.with_context(active_model='stock.picking',
                                        active_id=self.picking.id,
                                        active_ids=[self.picking.id]
                                        ).create({})
        line = wiz.print_label_lines[:1]
        line.ul_id = self.ul_id
        line.onchange_package_id()
        self.assertEqual(line.package_qty, (line.quant_id.qty / 10))
