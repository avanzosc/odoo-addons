# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProductVatPrice(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductVatPrice, cls).setUpClass()
        cls.product_obj = cls.env['product.template']
        cls.tax = cls.env['account.tax'].search([], limit=1)
        cls.product_vals = {
            'name': 'aaaa',
            'list_price': 100,
            'taxes_id': cls.tax
            }
        cls.product = cls.env['product.template'].create(cls.product_vals)

    def test_product_vat_price(self):
        self.assertEqual(self.product.vat_price, 100 + self.tax.amount)
        self.product.list_price = 200
        self.product.onchange_vat_price()
        self.assertEqual(self.product.vat_price, 200 + 2 * self.tax.amount)
