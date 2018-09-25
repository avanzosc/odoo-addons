# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import UserError


class TestSalePricelistLimit(common.TransactionCase):

    def setUp(self):
        super(TestSalePricelistLimit, self).setUp()
        self.sale_order_model = self.env['sale.order']
        self.partner_model = self.env['res.partner']
        self.partner1 = self.partner_model.create({
            'name': 'Partner1',
            })
        self.partner2 = self.partner_model.create({
            'name': 'Partner2',
            })
        self.product = self.env.ref('product.product_product_2')
        self.product2 = self.env.ref('product.product_product_4')
        self.sale_order1 = self.sale_order_model.create({
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {'product_id': self.product.id})],
            })
        self.sale_order2 = self.sale_order_model.create({
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {'product_id': self.product2.id})],
            })
        self.test_pricelist = self.partner1.property_product_pricelist.copy(
            {'name': 'Test Pricelist',
             'has_limit': True,
             'limit_amount': 200})
        self.partner1.property_product_pricelist = self.test_pricelist
        self.partner2.property_product_pricelist = self.test_pricelist

    def test_sale_pricelist_limit(self):
        self.sale_order1.action_confirm()
        with self.assertRaises(UserError):
            # Amount exceeded
            self.sale_order2.action_confirm()
