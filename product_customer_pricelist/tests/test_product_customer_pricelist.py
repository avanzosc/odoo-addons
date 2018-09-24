# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProductCustomerPricelist(common.TransactionCase):

    def setUp(self):
        super(TestProductCustomerPricelist, self).setUp()
        self.sale_order_model = self.env['sale.order']
        self.partner_model = self.env['res.partner']
        self.partner1 = self.partner_model.create({
            'name': 'Partner1',
            })
        self.product = self.env.ref('product.product_product_4')
        self.sale_order = self.sale_order_model.create({
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {'product_id': self.product.id, })],
            })
        self.test_pricelist = self.partner1.property_product_pricelist.copy(
            {'name': 'Test Pricelist'})
        self.product.property_product_pricelist_id = self.test_pricelist

    def test_product_customer_pricelist(self):
        self.assertNotEqual(self.partner1.property_product_pricelist,
                            self.test_pricelist, 'Error, pricelist does match')
        self.sale_order.action_confirm()
        self.assertEqual(self.partner1.property_product_pricelist,
                         self.test_pricelist,
                         'Error, pricelist does not match')
