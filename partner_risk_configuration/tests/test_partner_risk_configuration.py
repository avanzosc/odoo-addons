# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import _


class TestPartnerRiskConfiguration(TransactionCase):

    def setUp(self):
        super(TestPartnerRiskConfiguration, self).setUp()
        self.partner_model = self.env['res.partner']
        self.config_obj = self.env['account.config.settings']
        self.product = self.env.ref('product.product_product_2')
        self.product.invoice_policy = 'order'
        self.parent_partner = self.partner_model.create({
            'name': 'Parent Partner test',
            'customer': True,
        })
        self.partner = self.partner_model.create({
            'name': 'Partner test',
            'customer': True,
            'parent_id': self.parent_partner.id,
        })
        self.journal = self.env['account.journal'].create({
            'type': 'sale',
            'name': 'Test Sales',
            'code': 'TSALE',
        })
        self.prod_account = self.env.ref('account.a_sale')
        self.inv_account = self.env.ref('account.a_recv')
        date_inv = datetime.now() - relativedelta(days=7)
        date_due = datetime.now() - relativedelta(days=3)
        self.invoice = self.env['account.invoice'].create({
            'journal_id': self.journal.id,
            'company_id': self.env.user.company_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'date_invoice': date_inv.strftime("%Y-%m-%d"),
            'date_due': date_due.strftime("%Y-%m-%d"),
            'partner_id': self.partner.id,
            'account_id': self.inv_account.id,
            'invoice_line': [(0, 0, {
                'account_id': self.prod_account.id,
                'name': 'Test line',
                'price_unit': 50,
                'quantity': 10,
            })]
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'pricelist_id': self.env.ref('product.list0').id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'product_uom': self.product.uom_id.id,
                'price_unit': 100.0})],
        })

    def test_unified_risk_boolean(self):
        self.parent_partner.unified_risk = True
        self.parent_partner.onchange_unified_risk()
        self.assertTrue(self.partner.unified_risk)
        self.parent_partner.unified_risk = False
        self.parent_partner.onchange_unified_risk()
        self.assertFalse(self.partner.unified_risk)

    def test_configuration_unified_risk_check(self):
        config = self.config_obj.new()
        config.unified_risk_default = True
        config.set_parameters()
        res = config.default_get(config._fields.keys())
        self.assertTrue(res.get('unified_risk_default', False))
        test_partner = self.partner_model.create({'name': 'Testing Creation',
                                                  'customer': True})
        self.assertTrue(test_partner.unified_risk)
        config.unified_risk_default = False
        config.set_parameters()
        res = config.default_get(config._fields.keys())
        self.assertFalse(res.get('unified_risk_default', False))
        test_partner = self.partner_model.create({'name': 'Testing Creation',
                                                  'customer': True})
        self.assertFalse(test_partner.unified_risk)

    def test_partner_computed_fields(self):
        self.parent_partner.unified_risk = False
        self.parent_partner.onchange_unified_risk()
        self.parent_partner.risk_invoice_draft_include = True
        self.partner.risk_invoice_draft_include = True
        self.parent_partner.risk_sale_order_include = True
        self.partner.risk_sale_order_include = True
        self.partner.credit_limit = 2000.0
        self.parent_partner.credit_limit = 2000.0
        self.sale_order.action_button_confirm()
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 500.0)
        self.assertAlmostEqual(self.partner.risk_sale_order, 100.0)
        self.assertAlmostEqual(self.partner.risk_total, 600.0)
        self.assertAlmostEqual(self.parent_partner.risk_invoice_draft, 0.0)
        self.assertAlmostEqual(self.parent_partner.risk_total, 0.0)
        self.assertAlmostEqual(self.parent_partner.risk_sale_order, 0.0)
        self.parent_partner.unified_risk = True
        self.parent_partner.onchange_unified_risk()
        self.assertAlmostEqual(self.parent_partner.risk_invoice_draft, 500.0)
        self.assertAlmostEqual(self.parent_partner.risk_sale_order, 100.0)
        self.assertAlmostEqual(self.parent_partner.risk_total, 600.0)

    def test_sale_risk(self):
        # TEST - partner sale risk #2
        sale = self.sale_order.copy()
        self.parent_partner.unified_risk = False
        self.parent_partner.onchange_unified_risk()
        self.partner.write({
            "risk_sale_order_limit": 75.0,
            "credit_limit": 150.0,
        })
        wiz_dic = sale.action_button_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         _("This sale order exceeds the sales orders risk.\n"))
        # TEST - partner sale risk #3
        sale1 = self.sale_order.copy()
        self.parent_partner.unified_risk = False
        self.parent_partner.onchange_unified_risk()
        self.parent_partner.write({
            "risk_sale_order_limit": 115.0,
            "credit_limit": 75.0,
            "risk_sale_order_include": True,
        })
        self.partner.write({
            "risk_sale_order_limit": 1000.0,
            "credit_limit": 5000.0,
            "risk_sale_order_include": True,
        })
        wiz_dic = sale1.action_button_confirm()
        self.assertEqual(wiz_dic, True)
        sale1.action_cancel()
        self.parent_partner.unified_risk = True
        self.parent_partner.onchange_unified_risk()
        sale1 = self.sale_order.copy()
        wiz_dic = sale1.action_button_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         _("This sale order exceeds the financial risk.\n"))
        # TEST - partner sale risk #4
        sale2 = self.sale_order.copy()
        self.parent_partner.write({
            "risk_sale_order_limit": 150.0,
            "credit_limit": 100.0,
            "risk_sale_order_include": True,
            "risk_invoice_draft_include": True,
        })
        wiz_dic = sale2.action_button_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg, _("Financial risk exceeded.\n"))

    def test_financial_risk(self):
        self.parent_partner.unified_risk = False
        self.parent_partner.onchange_unified_risk()
        self.partner.risk_invoice_draft_include = True
        self.partner.risk_invoice_unpaid_include = True
        self.partner.credit_limit = 1000.0
        self.invoice.signal_workflow('invoice_open')
        self.partner.risk_invoice_unpaid_limit = 499.0
        invoice2 = self.invoice.copy()
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg, _("Financial risk exceeded.\n"))
        self.partner.risk_invoice_unpaid_limit = 0.0
        self.partner.risk_invoice_open_limit = 300.0
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         _("This invoice exceeds the open invoices risk.\n"))
        self.partner.risk_invoice_open_limit = 0.0
        self.partner.risk_invoice_draft_include = False
        self.partner.risk_invoice_open_include = True
        self.partner.credit_limit = 900.0
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         _("This invoice exceeds the financial risk.\n"))
        self.parent_partner.unified_risk = True
        self.parent_partner.onchange_unified_risk()
        self.parent_partner.risk_invoice_open_limit = 0.0
        self.parent_partner.credit_limit = 1000.0
        self.parent_partner.risk_invoice_unpaid_limit = 499.0
        self.parent_partner.risk_invoice_draft_include = True
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg, _("Financial risk exceeded.\n"))
        self.parent_partner.risk_invoice_unpaid_limit = 0.0
        self.parent_partner.risk_invoice_open_limit = 300.0
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         _("This invoice exceeds the open invoices risk.\n"))
        self.parent_partner.risk_invoice_open_limit = 0.0
        self.parent_partner.risk_invoice_draft_include = False
        self.parent_partner.risk_invoice_open_include = True
        self.parent_partner.credit_limit = 450.0
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         _("This invoice exceeds the financial risk.\n"))
        self.parent_partner.credit_limit = 5000.0
        wiz_dic = invoice2.invoice_open()
        self.assertFalse('res_model' in wiz_dic)
        invoice3 = self.invoice.copy()
        self.parent_partner.risk_invoice_open_limit = 10.0
        self.parent_partner.credit_limit = 10.0
        self.parent_partner.risk_invoice_unpaid_limit = 10.0
        wiz_dic = invoice3.with_context(bypass_risk=True).invoice_open()
        self.assertFalse('res_model' in wiz_dic)
