# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestPurchaseProductVariants(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseProductVariants, self).setUp()
        self.purchase_line_model = self.env['purchase.order.line']
        self.product = self.env['product.product'].create({
            'name': 'Length / Distance product',
            'uom_id': self.ref('product.product_uom_meter'),
            'uom_po_id': self.ref('product.product_uom_km'),
            'uop_id': self.ref('product.product_uom_cm'),
            'uop_coeff': 100000.0,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'supplier': True,
            'property_product_pricelist_purchase': self.ref('purchase.list0'),
        })

    def test_onchange_product_id(self):
        line = self.purchase_line_model.new()
        line.product_id = self.product
        result = line.onchange_product_id(
            self.partner.property_product_pricelist_purchase.id,
            line.product_id.id, 1.0, line.product_uom.id, self.partner.id)
        self.assertNotEquals(line.product_uom, self.product.uom_po_id)
        self.assertNotEquals(line.product_uom, self.product.uom_id)
        self.assertEquals(
            result['value']['product_uom'], self.product.uom_po_id.id)
        self.assertEquals(
            result['value']['product_uop'], self.product.uop_id.id)
