# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo import fields
from odoo.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class TestSupplierinfoUpdate(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSupplierinfoUpdate, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.supplierinfo_model = cls.env['product.supplierinfo']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.purchase_model = cls.env['purchase.order']
        cls.supplier = cls.partner_model.create({
            'name': 'Supplier1',
            'supplier': 'True',
        })
        cls.seller = cls.supplierinfo_model.create({
            'name': cls.supplier.id,
            'price': 12.0,
        })
        cls.seller_2 = cls.supplierinfo_model.create({
            'name': cls.supplier.id,
            'price': 10.0,
            'min_qty': 50,
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'type': 'product',
            'seller_ids': [(6, 0, [cls.seller.id])],
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.product_2 = cls.product_model.create({
            'name': 'Product_2',
            'type': 'product',
            'default_code': 'P2',
            'seller_ids': [(6, 0, [cls.seller_2.id])],
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })

    def test_supplierinfo_price_update(self):
        purchase = self.purchase_model.create({
            'partner_id': self.supplier.id,
            'order_line': [
                (0, 0, {
                    'name': self.product.name,
                    'product_id': self.product.id,
                    'product_qty': 10.0,
                    'product_uom': self.product.uom_po_id.id,
                    'price_unit': self.product.standard_price,
                    'date_planned': fields.Date.today(),
                })],
        })
        order_line = purchase.order_line[:1]
        self.assertNotEquals(
            self.product.standard_price, self.seller.price,
            "Product's cost price must be different from seller's price")
        self.assertNotEquals(
            order_line.price_unit, self.seller.price,
            "Purchase line unit price must be different from seller's price")
        order_line._onchange_quantity()
        self.assertEquals(
            order_line.price_unit, self.seller.price,
            "The product's price on the purchase line is not correct.")
        order_line.price_unit = 10.0
        sellers_price = self.seller.price
        self.assertNotEquals(
            order_line.price_unit, sellers_price,
            "Purchase line unit price must be different from seller's price")
        purchase.button_confirm()
        self.assertNotEquals(
            self.seller.price, sellers_price,
            "Seller's price hasn't been updated")
        self.assertEqual(order_line.price_unit, self.seller.price,
                         'The price on the purchase order line and seller '
                         'price is not the same.')

    def test_seller_price_error(self):
        purchase = self.purchase_model.create({
            'partner_id': self.supplier.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_2.name,
                    'product_id': self.product_2.id,
                    'product_qty': 10.0,
                    'product_uom': self.product_2.uom_po_id.id,
                    'price_unit': self.product_2.standard_price,
                    'date_planned': fields.Date.today(),
                })],
        })
        with self.assertRaises(ValidationError):
            purchase.button_confirm()
