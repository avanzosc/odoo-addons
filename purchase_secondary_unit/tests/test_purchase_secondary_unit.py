# Copyright 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import odoo.tests.common as common
from odoo.exceptions import ValidationError


class TestPurchaseProductVariants(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseProductVariants, self).setUp()
        self.purchase_line_model = self.env['purchase.order.line']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'supplier': True,
        })
        self.product = self.env['product.product'].create({
            'name': 'Length / Distance product',
            'uom_id': self.ref('product.product_uom_meter'),
            'uom_po_id': self.ref('product.product_uom_km'),
            'uop_id': self.ref('product.product_uom_cm'),
            'uop_coeff': 100000.0,
            'seller_ids': [(0, 0, {
                'name': self.partner.id,
                'min_qty': 1.0,
                'price': 10.0,
            })]
        })

    def test_uop_id_constraint(self):
        with self.assertRaises(ValidationError):
            self.product.write({
                'uop_id': self.ref('product.product_uom_kgm'),
            })
        self.product.write({
            'uop_id': self.ref('product.product_uom_km'),
        })

    def test_onchange_product_id(self):
        line = self.purchase_line_model.new()
        line.product_id = self.product
        line.onchange_product_id()
        self.assertEquals(line.product_uom, self.product.uom_po_id)
        self.assertEquals(line.product_uop, self.product.uop_id)
        self.assertEquals(line.product_uop_coeff, self.product.uop_coeff)
