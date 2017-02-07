# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestSaleOrderLineAddWebsite(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineAddWebsite, self).setUp()
        self.instance_obj = self.env['account.analytic.plan.instance']
        self.analytic_account_obj = self.env['account.analytic.account']
        self.instance_line_obj = \
            self.env['account.analytic.plan.instance.line']
        self.website = self.env['website.sale'].create({
            'name': 'www.avanzosc.es'
        })
        self.sale_line = self.env.ref('sale.sale_order_line_7')
        self.product = self.env.ref('product.product_product_3')
        self.sale_line.website_id = self.website
        self.order_id = self.sale_line.order_id

    def test_onchange_website(self):
        with self.assertRaises(exceptions.Warning):
            self.sale_line._onchange_website_id()
        self.plan = self.env['account.analytic.plan'].create({
            'name': 'Test plan',
        })
        self.sale_line._onchange_website_id()
        name = u'{}-{}'.format(
            self.sale_line.product_id.name, self.website.name)
        instance_id = self.instance_obj.search([('name', '=', name)])
        self.assertTrue(instance_id)
        self.assertTrue(instance_id, self.sale_line.analytics_id)
        product_account = self.analytic_account_obj.search([
            ('name', '=', self.sale_line.product_id.name)])
        self.assertTrue(product_account)
        self.assertTrue(self.instance_line_obj.search([
            ('plan_id', '=', instance_id.id),
            ('analytic_account_id', '=', product_account[0].id)]))
        website_account = self.analytic_account_obj.search([
            ('name', '=', self.website.name)])
        self.assertTrue(website_account)
        self.assertTrue(self.instance_line_obj.search([
            ('plan_id', '=', instance_id.id),
            ('analytic_account_id', '=', website_account[0].id)]))

    def test_onchange_product_id(self):
        self.plan = self.env['account.analytic.plan'].create({
            'name': 'Test plan',
        })
        self.sale_line.product_id = self.product
        res = self.sale_line.product_id_change_with_wh(
            self.order_id.pricelist_id.id, self.product.id,
            qty=self.sale_line.product_uom_qty, uom=False,
            qty_uos=self.sale_line.product_uos_qty, uos=False,
            name=self.product.name, partner_id=self.order_id.partner_id.id,
            lang=False, update_tax=True, date_order=self.order_id.date_order,
            packaging=self.sale_line.product_packaging,
            fiscal_position=self.order_id.fiscal_position,
            flag=False, warehouse_id=self.order_id.warehouse_id.id)
        prod_name = self.product.name
        web_name = self.website.name
        name = u'{}-{}'.format(prod_name, web_name)
        plan = self.instance_obj.search([('name', '=', name)])
        self.assertEqual(res['value']['analytics_id'], plan.id)
        self.sale_line.write({'analytics_id': res['value']['analytics_id']})
        self.assertEqual(len(plan.account_ids), 2)
        self.assertTrue(plan.account_ids.filtered(
            lambda x: x.analytic_account_id.name == prod_name))
        self.assertTrue(plan.account_ids.filtered(
            lambda x: x.analytic_account_id.name == web_name))
