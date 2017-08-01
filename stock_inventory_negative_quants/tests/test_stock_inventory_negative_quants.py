# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockInventoryNegativeQuant(common.TransactionCase):

    def setUp(self):
        super(TestStockInventoryNegativeQuant, self).setUp()
        self.quant_model = self.env['stock.quant']
        self.wiz_model = self.env['stock.change.product.qty']
        self.product = self.env['product.product'].create({
            'name': 'Product Test',
            'type': 'product',
        })
        self.location = self.ref('stock.stock_location_stock')
        self.quant1 = self.quant_model.sudo().create({
            'product_id': self.product.id,
            'qty': 100.0,
            'location_id': self.location,
        })
        self.quant2 = self.quant_model.sudo().create({
            'product_id': self.product.id,
            'qty': -100.0,
            'location_id': self.location,
        })
        self.wiz = self.wiz_model.with_context(
            active_model='product.product', active_id=self.product.id,
            active_ids=[self.product.id]).create({})

    def test_wizard_no_deleting_negative_quants(self):
        self.wiz.write({'delete_negative_quants': False,
                        'new_quantity': 0})
        self.wiz.change_product_qty()
        quants = self.quant_model.search([('product_id', '=', self.product.id),
                                          ('qty', '<', 0)])
        self.assertTrue(quants)

    def test_wizard_deleting_negative_quants(self):
        self.wiz.write({'delete_negative_quants': True,
                        'new_quantity': 0})
        self.wiz.change_product_qty()
        quants = self.quant_model.search([('product_id', '=', self.product.id),
                                          ('qty', '<', 0)])
        self.assertFalse(quants)
