# -*- coding: utf-8 -*-
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestProductSequenceByCategory(common.TransactionCase):

    def setUp(self):
        super(TestProductSequenceByCategory, self).setUp()
        self.product_model = self.env['product.product']
        self.template_model = self.env['product.template']
        self.category_model = self.env['product.category']
        self.sequence_model = self.env['ir.sequence']
        self.seq1 = self.sequence_model.create({
            'name': 'Sequence 1',
            'prefix': 'PRE',
        })
        self.seq2 = self.sequence_model.create({
            'name': 'Sequence 2',
            'suffix': 'SUF',
        })
        self.categ1 = self.category_model.create({
            'name': 'Category 1',
            'sequence_id': self.seq1.id,
        })
        self.categ2 = self.category_model.create({
            'name': 'Category 2',
            'sequence_id': self.seq2.id,
        })
        self.categ3 = self.category_model.create({
            'name': 'Category 3',
            'sequence_id': self.seq2.id,
        })

    def test_new_product_product(self):
        code = self._get_next_code(self.categ1.sequence_id)
        product = self.product_model.create({
            'name': 'New Product',
            'categ_id': self.categ1.id,
        })
        self.assertTrue(product.default_code)
        self.assertEqual(product.default_code, code)
        self.assertEqual(product.product_tmpl_id.default_code, code)
        product.write({
            'categ_id': self.categ2.id,
        })
        self.assertEqual(product.default_code, code)
        new_code = self._get_next_code(self.categ3.sequence_id)
        product.write({
            'categ_id': self.categ3.id,
            'default_code': False,
        })
        self.assertNotEqual(product.default_code, code)
        self.assertEqual(product.default_code, new_code)
        self.assertEqual(product.product_tmpl_id.default_code, new_code)

    def test_new_product_template(self):
        code = self._get_next_code(self.categ2.sequence_id)
        template = self.template_model.create({
            'name': 'New Product',
            'categ_id': self.categ2.id,
        })
        self.assertTrue(template.default_code)
        self.assertEqual(template.default_code, code)
        self.assertEqual(template.product_variant_ids[:1].default_code, code)
        template.write({
            'categ_id': self.categ3.id,
        })
        self.assertEqual(template.default_code, code)
        new_code = self._get_next_code(self.categ1.sequence_id)
        template.write({
            'categ_id': self.categ1.id,
            'default_code': False,
        })
        self.assertNotEqual(template.default_code, code)
        self.assertEqual(template.default_code, new_code)
        self.assertEqual(template.product_variant_ids[:1].default_code,
                         new_code)

    def _get_next_code(self, sequence):
        d = self.sequence_model._interpolation_dict()
        prefix = self.sequence_model._interpolate(
            sequence.prefix, d)
        suffix = self.sequence_model._interpolate(
            sequence.suffix, d)
        code = (prefix + ('%%0%sd' % sequence.padding %
                          sequence.number_next_actual) + suffix)
        return code
