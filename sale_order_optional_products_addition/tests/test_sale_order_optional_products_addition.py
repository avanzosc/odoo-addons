# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common, SavepointCase


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderOptionalProductsAddition(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_model = cls.env['sale.order']
        cls.sale_line_model = cls.env['sale.order.line']
        cls.product_model = cls.env['product.product']
        cls.partner = cls.env['res.partner'].create({'name': 'Test'})
        cls.sale = cls.sale_model.create({
            'partner_id': cls.partner.id
        })
        cls.product1 = cls.product_model.create({
            'name': 'Product1',
            'type': 'service',
        })
        cls.product2 = cls.product_model.create({
            'name': 'Product2',
            'type': 'service',
            'optional_product_product_ids': [(6, 0, [cls.product1.id])]
        })
        cls.product3 = cls.product_model.create({
            'name': 'Product3',
            'type': 'service',
            'optional_product_product_ids': [(6, 0, [cls.product2.id])]
        })

    def test_test_sale_order_optional_products_addition(self):
        self.sale_line_model.create({
            'product_id': self.product2.id,
            'order_id': self.sale.id,
            'name': 'Test line description',
        })
        self.sale.onchange_order_line()
        self.assertTrue(len(self.sale.sale_order_option_ids) == 1)
        self.assertEqual(self.sale.sale_order_option_ids[
                             0].product_id, self.product1)
        self.sale_line_model.create({
            'product_id': self.product3.id,
            'order_id': self.sale.id,
            'name': 'Test line description',
        })
        self.sale.onchange_order_line()
        self.assertTrue(len(self.sale.sale_order_option_ids) == 2)
        self.assertEqual(self.sale.sale_order_option_ids[
                             0].product_id, self.product1)
        self.assertEqual(self.sale.sale_order_option_ids[
                             1].product_id, self.product2)
