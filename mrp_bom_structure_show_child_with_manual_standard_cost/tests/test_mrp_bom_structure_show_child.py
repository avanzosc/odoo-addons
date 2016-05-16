# -*- coding: utf-8 -*-
# (c) 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestMrpBomStructureShowChild(TransactionCase):

    def setUp(self):
        super(TestMrpBomStructureShowChild, self).setUp()
        product_obj = self.env['product.product']
        mrp_bom_obj = self.env['mrp.bom']
        self.price = 5
        bom_product = product_obj.create({
            'name': 'Test product',
            'manual_standard_cost': self.price,
        })
        self.bom_line_product = product_obj.create({
            'name': 'Test product 1',
            'manual_standard_cost': 2 * self.price,
        })
        child_bom_line_product = product_obj.create({
            'name': 'Test product 2',
            'manual_standard_cost': 3 * self.price,
        })
        self.bom = mrp_bom_obj.create({
            'type': 'phantom',
            'product_id': bom_product.id,
            'product_tmpl_id': bom_product.product_tmpl_id.id,
            'bom_line_ids': [(0, 0, {'product_id': self.bom_line_product.id})]
        })
        mrp_bom_obj.create({
            'product_id': self.bom_line_product.id,
            'product_tmpl_id': self.bom_line_product.product_tmpl_id.id,
            'bom_line_ids': [(0, 0, {'product_id': child_bom_line_product.id})]
        })

    def test_bom_lines_manual_standard_cost(self):
        self.assertEqual(self.bom.bom_line_ids[:1].product_id,
                         self.bom_line_product)
        self.assertEqual(self.bom.bom_line_ids[:1].manual_standard_cost,
                         2 * self.price)
        self.assertEqual(self.bom.bom_line_ids[:1].childs_manual_standard_cost,
                         3 * self.price)
