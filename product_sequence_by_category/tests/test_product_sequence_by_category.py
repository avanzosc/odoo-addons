# Copyright 2015-2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestProductSequenceByCategory(TransactionCase):

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

    def test_rewrite_code_product(self):
        code = self._get_next_code(self.categ1.sequence_id, cont=1)
        product = self.product_model.create({
            'name': 'New Product',
            'categ_id': self.categ1.id,
        })
        self.assertEqual(product.default_code, code)
        new_code = self._get_next_code(self.categ1.sequence_id, cont=2)
        product.rewrite_product_default_code()
        self.assertNotEqual(product.default_code, code)
        self.assertEqual(product.default_code, new_code)
        self.categ1.write({
            'sequence_id': False,
        })
        product.rewrite_product_default_code()
        self.assertEqual(product.default_code, new_code)
        categ2_code = self._get_next_code(self.categ2.sequence_id)
        product.write({
            'categ_id': self.categ2.id,
        })
        self.assertEqual(product.default_code, new_code)
        product.rewrite_product_default_code()
        self.assertEqual(product.default_code, categ2_code)

    def test_rewrite_code_template(self):
        code = self._get_next_code(self.categ1.sequence_id)
        template = self.template_model.create({
            'name': 'New Product',
            'categ_id': self.categ1.id,
        })
        self.assertEqual(template.default_code, code)
        new_code = self._get_next_code(self.categ1.sequence_id)
        template.rewrite_template_default_code()
        self.assertNotEqual(template.default_code, code)
        self.assertEqual(template.default_code, new_code)
        self.categ1.write({
            'sequence_id': False,
        })
        template.rewrite_template_default_code()
        self.assertEqual(template.default_code, new_code)
        categ2_code = self._get_next_code(self.categ2.sequence_id)
        template.write({
            'categ_id': self.categ2.id,
        })
        self.assertEqual(template.default_code, new_code)
        template.rewrite_template_default_code()
        self.assertEqual(template.default_code, categ2_code)

    def _get_next_code(self, sequence, cont=0):
        prefix, suffix = sequence._get_prefix_suffix()
        if not cont:
            cont = sequence.number_next_actual
        code = (prefix + ('%%0%sd' % sequence.padding % cont) + suffix)
        return code
