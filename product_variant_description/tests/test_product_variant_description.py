# -*- coding: utf-8 -*-
# (c) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestProductVariantDescription(TransactionCase):

    def setUp(self):
        super(TestProductVariantDescription, self).setUp()
        self.pricelist = self.ref('product.list0')
        self.product_obj = self.env['product.product']
        self.so_line_model = self.env['sale.order.line']
        self.partner = self.ref('base.res_partner_1')
        self.fp = self.ref('account.fiscal_position_normal_taxes_template1')

    def test_product_id_change(self):
        product = self.product_obj.create({
            'name': 'Test product',
            'variant_description': 'Product variant description test'
        })
        res = self.so_line_model.product_id_change(
            self.pricelist, product.id, partner_id=self.partner,
            fiscal_position=self.fp)
        self.assertEqual(
            u'[{}] {}'.format(product.variant_description,
                             product.name), res['value']['name'])
