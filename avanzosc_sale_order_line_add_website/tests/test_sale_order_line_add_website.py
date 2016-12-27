# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestSaleOrderLineAddWebsite(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderLineAddWebsite, self).setUp()
        self.plan = self.env['account.analytic.plan'].create({
            'name': 'Test plan',
        })
        self.instance_obj = self.env['account.analytic.plan.instance']
        self.analytic_account_obj = self.env['account.analytic.account']
        self.instance_line_obj = \
            self.env['account.analytic.plan.instance.line']
        self.website = self.env['website.sale'].create({
            'name': 'www.avanzosc.es'
        })
        self.sale_line = self.env.ref('sale.sale_order_line_7')

    def test_onchange_website(self):
        self.sale_line.website_id = self.website
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
