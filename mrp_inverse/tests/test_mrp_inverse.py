# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpInverse(common.TransactionCase):

    def setUp(self):
        super(TestMrpInverse, self).setUp()
        self.production_model = self.env['mrp.production']
        self.produce_product = self.ref('product.product_product_17')
        self.consume_product = self.ref('product.product_product_18')
        self.bom_id = self.env.ref('mrp.mrp_bom_1')
        self.bom_id.product_id = self.consume_product
        self.bom_id.inverse = True
        res = self.bom_id.create_mrp_production()
        production_id = res['res_id']
        self.production = self.production_model.browse(production_id)

    def test_create_production(self):
        self.assertTrue(self.production.inverse, 'Inverse field not loaded')
        self.bom_id.inverse = False
        res = self.production.bom_id_change(self.bom_id.id)
        self.assertFalse(res.get('value', {}).get('inverse', True),
                         'Onchange inverse')
        self.production.inverse = True
        self.production.action_confirm()
        consume_lines = self.production.move_lines.filtered(
            lambda x: x.product_id.id == self.consume_product)
        produce_lines = self.production.move_created_ids.filtered(
            lambda x: x.product_id.id == self.produce_product)
        self.assertTrue(bool(consume_lines), 'Consume lines not inverted')
        self.assertTrue(bool(produce_lines), 'Produce lines not inverted')

    def test_wizard_inverse_production(self):
        self.production.action_confirm()
        wiz_model = self.env['inverse.mrp.product.produce']
        wiz = wiz_model.with_context(active_model='mrp.production',
                                     active_id=self.production.id,
                                     active_ids=self.production.ids).create({})
        self.assertEqual(wiz.product_id.id, self.consume_product,
                         'Inverse wizard product incorrect,')
        self.assertEqual(wiz.product_qty, self.production.product_qty,
                         'Inverse wizard qty incorrect.')
        line = wiz.consume_lines.filtered(lambda x: x.product_id.id ==
                                          self.produce_product)
        self.assertTrue(bool(line), 'Inverse wizard lines incorrect.')
        line.write({'product_qty': wiz.product_qty})
        self.assertFalse(wiz.need_confirm, 'Qty check not correct.')
        line.write({'product_qty': 100})
        self.assertTrue(wiz.need_confirm, 'Qty check not correct.')
        wiz.do_produce()
        consume_lines = self.production.move_lines2.filtered(
            lambda x: x.product_id.id == self.consume_product)
        produce_lines = self.production.move_created_ids2.filtered(
            lambda x: x.product_id.id == self.produce_product)
        self.assertTrue(bool(consume_lines), 'Consume lines not inverted')
        self.assertTrue(bool(produce_lines), 'Produce lines not inverted')
