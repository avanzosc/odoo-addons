# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProductUpgradeSaleCostPrice(common.TransactionCase):

    def setUp(self):
        super(TestProductUpgradeSaleCostPrice, self).setUp()
        self.wiz_model = self.env['wiz.product.upgrade.prices']
        self.product = self.browse_ref('product.product_product_24')
        self.product.write({'lst_price': 200.0,
                            'standard_price': 200.0})

    def test_product_upgrade_sale_cost_price_increase(self):
        wiz = self.wiz_model.create({})
        wiz.increase_sale_price = False
        wiz.onchange_increase_sale_price()
        self.assertEqual(
            wiz.sale_increase, 0, 'Sale increase must be 0')
        wiz.increase_sale_price = True
        wiz.onchange_increase_sale_price()
        self.assertEqual(
            wiz.sale_increase, 0.014, 'Sale increase must be 0.014')
        wiz.increase_cost_price = False
        wiz.onchange_increase_cost_price()
        self.assertEqual(
            wiz.cost_increase, 0, 'Cost increase must be 0')
        wiz.increase_cost_price = True
        wiz.onchange_increase_cost_price()
        self.assertEqual(
            wiz.cost_increase, 0.014, 'Cost increase must be 0.014')
        wiz.with_context(
            {'active_ids':
             self.product.ids}).update_product_prices()
        self.assertEqual(
            self.product.lst_price, 202.8, 'Error in list price increase')
        self.assertEqual(
            self.product.standard_price, 202.8,
            'Error in standard price increase')

    def test_product_upgrade_sale_cost_price_decremented(self):
        wiz = self.wiz_model.create({})
        wiz.update({'sale_increase': -0.014,
                    'cost_increase': -0.014})
        wiz.with_context(
            {'active_ids':
             self.product.ids}).update_product_prices()
        self.assertEqual(
            round(self.product.lst_price, 2), 197.20,
            'Error in list price increase')
        self.assertEqual(
            round(self.product.standard_price, 2), 197.20,
            'Error in standard price increase')
