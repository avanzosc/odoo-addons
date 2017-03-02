# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestQualityControlByProduct(common.TransactionCase):

    def setUp(self):
        super(TestQualityControlByProduct, self).setUp()
        self.test_model = self.env['qc.test']
        self.picking_type_model = self.env['stock.picking.type']
        self.qc_trigger_model = self.env['qc.trigger']
        self.qc_trigger_line_model = self.env['qc.trigger.product_line']
        self.picking_model = self.env['stock.picking']

        self.test = self.env.ref('quality_control.qc_test_1')
        test_vals = {
            'name': 'Empty test',
            'type': 'generic',
            'active': True,
            'category':
                self.ref('quality_control.qc_test_template_category_generic')
            }
        self.empty_test = self.test_model.create(test_vals)
        self.product = self.env.ref('product.product_product_3')
        self.partner = self.env.ref('base.res_partner_2')

        self.picking_type_out = self.env.ref('stock.picking_type_out')
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.trigger_in = self.qc_trigger_model.search(
            [('picking_type', '=', self.picking_type_in.id)])
        self.trigger_in_line = self.qc_trigger_line_model.create(
            {'product': self.product.id, 'test': self.test.id,
             'trigger': self.trigger_in.id})
        self.trigger_out = self.qc_trigger_model.search(
            [('picking_type', '=', self.picking_type_out.id)])
        self.trigger_out_line = self.qc_trigger_line_model.create(
            {'product': self.product.id, 'test': self.test.id,
             'trigger': self.trigger_out.id})

        self.lot = self.env['stock.production.lot'].create({
            'name': 'Lot for tests',
            'product_id': self.product.id,
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
            'picking_type_id': self.picking_type_in.id,
            'move_lines': [(0, 0, move_in_vals)],
        })
        move_out_vals = {
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 2.0,
            'restrict_lot_id': self.lot.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_out.default_location_dest_id.id,
        }
        self.picking_out = self.picking_model.create({
            'picking_type_id': self.picking_type_out.id,
            'move_lines': [(0, 0, move_out_vals)],
        })
        self.picking_in.action_confirm()
        self.picking_in.force_assign()
        mv = self.picking_in.move_lines
        pack_datas = {
            'product_id': mv.product_id.id,
            'product_uom_id': mv.product_uom.id,
            'product_qty': mv.product_uom_qty,
            'lot_id': mv.restrict_lot_id.id,
            'location_id': mv.location_id.id,
            'location_dest_id': mv.location_dest_id.id,
            'date': mv.date,
            'picking_id': self.picking_in.id
        }
        self.env['stock.pack.operation'].create(pack_datas)
        self.picking_in.do_transfer()

    def test_product_onchange(self):
        self.test.product_id = self.product
        self.test.onchange_product()
        self.assertEqual(self.test.product_tmpl_id,
                         self.product.product_tmpl_id,
                         'Product Template not correctly set.')
        self.assertEqual(self.product.qc_test_count, 1,
                         'Test count in product')
        self.assertEqual(self.product.product_tmpl_id.qc_test_count, 1,
                         'Test count in product template')

    def test_partner_onchange(self):
        self.assertEqual(self.partner.qc_test_count, 0,
                         'Test count in partner.')
        self.test.partner_id = self.partner
        self.empty_test.partner_id = self.partner
        self.assertEqual(self.partner.qc_test_count, 2,
                         'Test count in partner.')

    def test_parent_onchange(self):
        self.empty_test.parent_id = self.test
        self.empty_test.onchange_parent()
        self.assertEqual(len(self.empty_test.test_lines),
                         len(self.test.test_lines),
                         'Not all test lines copied in parent onchange.')
        for line in self.test.test_lines:
            test_line = self.empty_test.test_lines.filtered(
                lambda x: (x.name == line.name and x.type == line.type))
            self.assertTrue(bool(test_line), 'Not line correctly copied.')

    def test_autoload_inspection_in_transfer_picking(self):
        in_inspection = self.picking_in.qc_inspections[:1]
        for line in in_inspection.inspection_lines:
            if line.test_line.type == 'qualitative':
                line.qualitative_value = line.possible_ql_values[:1]
            elif line.test_line.type == 'quantitative':
                line.quantitative_value = (line.min_value +
                                           ((line.max_value - line.min_value) /
                                            2))
        self.picking_out.action_confirm()
        self.picking_out.action_assign()
        self.picking_out.do_prepare_partial()
        self.picking_out.do_transfer()
        out_inspection = self.picking_out.qc_inspections[:1]
        for line in out_inspection.inspection_lines:
            in_line = in_inspection.inspection_lines.filtered(
                lambda x: x.test_line == line.test_line)
            self.assertEqual(in_line.quantitative_value,
                             line.quantitative_value,
                             'Quantitative value not autoloaded.')
            self.assertEqual(in_line.qualitative_value, line.qualitative_value,
                             'Qualitative value not autoloaded.')

    def test_create_trigger(self):
        wizard_obj = self.env['create.trigger.lines.wizard']
        self.assertFalse(self.empty_test.has_trigger_lines)
        self.empty_test.write(
            {'partner_id': self.partner.id,
             'product_tmpl_id': self.product.product_tmpl_id.id})
        wiz = wizard_obj.with_context(active_id=self.empty_test.id,
                                      active_ids=[self.empty_test.id]).create(
            {'trigger': self.trigger_out.id})
        wiz.create_trigger_lines()
        self.assertTrue(self.empty_test.has_trigger_lines)
        self.empty_test.template_trigger_line_ids.unlink()
        self.assertFalse(self.empty_test.has_trigger_lines)
        self.empty_test.product_id = self.product
        wiz = wizard_obj.with_context(active_id=self.empty_test.id,
                                      active_ids=[self.empty_test.id]).create(
            {'trigger': self.trigger_out.id})
        wiz.create_trigger_lines()
        self.assertTrue(self.empty_test.has_trigger_lines)
        self.assertFalse(self.empty_test.template_trigger_line_ids)
        self.assertTrue(self.empty_test.product_trigger_line_ids)

    def test_get_trigger_by_product(self):
        trigger_line_pool = self.env['qc.trigger.product_line']
        self.trigger_out2_line = self.qc_trigger_line_model.create(
            {'product': self.product.id, 'test': self.empty_test.id,
             'trigger': self.trigger_out.id})
        res = trigger_line_pool.get_trigger_line_for_product(
            self.trigger_out, self.product)
        self.assertEqual(len(res), 2)
        self.empty_test.parent_id = self.test
        self.empty_test.onchange_parent()
        res = trigger_line_pool.get_trigger_line_for_product(
            self.trigger_out, self.product)
        self.assertEqual(len(res), 1)
