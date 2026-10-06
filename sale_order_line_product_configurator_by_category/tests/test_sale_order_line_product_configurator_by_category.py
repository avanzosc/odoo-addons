# Copyright 2019 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class SaleOrderLineProductConfiguratorTest(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleOrderLineProductConfiguratorTest, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.category_model = cls.env['product.category']
        cls.sale_model = cls.env['sale.order']
        cls.partner_model = cls.env['res.partner']
        cls.category1 = cls.category_model.create({
            'name': 'Category1'
        })
        cls.category2 = cls.category_model.create({
            'name': 'Category2',
            'restricted_by': [(6, 0, [cls.category1.id])],
        })
        cls.category3 = cls.category_model.create({
            'name': 'Category3',
            'restricted_by': [(6, 0, [cls.category2.id])],
        })
        cls.product1 = cls.product_model.create({
            'name': 'Product1',
            'categ_id': cls.category1.id,
        })
        cls.product2 = cls.product_model.create({
            'name': 'Product2',
            'categ_id': cls.category2.id,
            'restricted_by_products': [(6, 0, [cls.product1.id])]
        })
        cls.product3 = cls.product_model.create({
            'name': 'Product3',
            'categ_id': cls.category3.id,
            'restricted_by_products': [(6, 0, [cls.product2.id])]
        })
        cls.product31 = cls.product_model.create({
            'name': 'Product31',
            'product_tmpl_id': cls.product3.product_tmpl_id.id,
            'categ_id': cls.category3.id,
        })
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.sale_order = cls.sale_model.create({
            'partner_id': cls.partner.id,
        })

        cls.line1 = cls.env['sale.order.line'].create({
            'product_id': cls.product1.id,
            'order_id': cls.sale_order.id,
        })
        cls.line2 = cls.env['sale.order.line'].create({
            'product_id': cls.product2.id,
            'order_id': cls.sale_order.id,
        })

    def test_product_id_onchange(self):
        res1 = self.line1.onchange_order_line()
        res2 = self.line2.onchange_order_line()
        self.assertEquals(res1['domain']['product_id'][0][2],
                          (self.product3.id,))
        self.assertEquals(res1, res2)

    def test_product_restrictions(self):
        self.assertEqual(self.product1.restricted_products._ids,
                         (self.product2.id,))
        self.assertEqual(self.product2.restricted_products._ids,
                         (self.product3.id,))
        self.assertEqual(self.product3.restricted_by_products._ids,
                         (self.product2.id,))
        self.product3.button_clear_restrictions()
        self.assertFalse(self.product3.restricted_by_products._ids)
        self.product3.button_category_restrict_products()
        self.assertEqual(self.product3.restricted_by_products._ids,
                         (self.product2.id,))
        self.assertFalse(self.product31.restricted_by_products._ids)
        self.product3.button_copy_to_siblings()
        self.assertEqual(self.product31.restricted_by_products._ids,
                         (self.product2.id,))
