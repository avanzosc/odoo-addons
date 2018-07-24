# -*- coding: utf-8 -*-
# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestProductVariantExtraPrice(common.TransactionCase):

    def setUp(self):
        super(TestProductVariantExtraPrice, self).setUp()
        self.setup_obj = self.env['base.config.settings']
        self.product_obj = self.env['product.product']
        product_vals = {'name': 'Product for test product_variant_extra_p'}
        self.product = self.product_obj.create(product_vals)

    def test_product_variant_extra_price_1(self):
        vals = {'number_price_field': '2'}
        setup = self.setup_obj.create(vals)
        setup._write_or_create_param('number.price.field', '2')
        self.assertEqual(self.product.number_price_field, '2',
                         'Bad value in product')

    def test_product_variant_extra_price_2(self):
        self.setup_obj._write_or_create_param('number.price.field', '2')
        value = self.setup_obj._get_parameter('number.price.field')
        self.assertNotEqual(value, False, 'Not value created')
        self.setup_obj._write_or_create_param('number.price.field', False)
        value = self.setup_obj._get_parameter('number.price.field')
        self.assertEqual(value, False, 'Bad value for field')
