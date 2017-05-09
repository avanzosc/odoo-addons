# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common
from openerp import exceptions


class TestHrTimesheetInvoiceByPartner(common.TransactionCase):
    def setUp(self):
        super(TestHrTimesheetInvoiceByPartner, self).setUp()
        self.config_obj = self.env['account.config.settings']
        self.analytic_acc_model = self.env['account.analytic.account']
        self.analytic_line_model = self.env['account.analytic.line']
        self.partner = self.env.ref('base.res_partner_2')
        pricelist = self.env.ref('product.list0')
        invoice_factor = self.env.ref(
            'hr_timesheet_invoice.timesheet_invoice_factor1')
        analytic_vals = {
            'name': 'Test Account #1',
            'partner_id': self.partner.id,
            'pricelist_id': pricelist.id,
            'to_invoice': invoice_factor.id,
            'state': 'open',
            }
        self.analytic_acc_1 = self.analytic_acc_model.create(analytic_vals)
        analytic_vals.update({'name': 'Test Account #2'})
        self.analytic_acc_2 = self.analytic_acc_model.create(analytic_vals)
        product = self.env.ref('product.product_product_2')
        line_vals = {
            'name': 'Analytic Invoicing Line #1',
            'account_id': self.analytic_acc_1.id,
            'general_account_id': self.ref('account.cash'),
            'to_invoice': invoice_factor.id,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'journal_id': self.ref('hr_timesheet.analytic_journal'),
            'user_id': self.ref('base.user_demo'),
            'amount': 100,
            'unit_amount': 20,
            }
        self.analytic_line_1 = self.analytic_line_model.create(line_vals)
        line_vals.update({'name': 'Analytic Invoicing Line #2',
                          'account_id': self.analytic_acc_2.id})
        self.analytic_line_2 = self.analytic_line_model.create(line_vals)
        self.invoice_create_wiz = self.env['hr.timesheet.invoice.create'
                                           ].with_context(
            active_id=self.analytic_line_1.id,
            active_ids=[self.analytic_line_1.id, self.analytic_line_2.id],
            active_model='account.analytic.line'
            )

    def test_normal_invoicing_process(self):
        config = self.config_obj.new()
        config.invoice_by_partner = False
        config.set_parameters()
        res = config.default_get(config._fields.keys())
        self.assertFalse(res.get('invoice_by_partner', False))
        wiz = self.invoice_create_wiz.create({})
        res = wiz.do_create()
        for rec in res['domain']:
            if rec[0] == 'id':
                self.assertEqual(len(rec[2]), 2)

    def test_by_partner_invoicing_process(self):
        config = self.config_obj.new()
        config.invoice_by_partner = True
        config.set_parameters()
        res = config.default_get(config._fields.keys())
        self.assertTrue(res.get('invoice_by_partner', False))
        wiz = self.invoice_create_wiz.create({})
        res = wiz.do_create()
        for rec in res['domain']:
            if rec[0] == 'id':
                self.assertEqual(len(rec[2]), 1)

    def test_raises(self):
        config = self.config_obj.new()
        config.invoice_by_partner = True
        config.set_parameters()
        factor = self.analytic_line_1.to_invoice.id
        self.analytic_line_1.to_invoice = False
        wiz = self.invoice_create_wiz.create({})
        with self.assertRaises(exceptions.Warning):
            wiz.do_create()
        self.analytic_line_1.to_invoice = factor
        self.analytic_acc_2.partner_id = False
        wiz = self.invoice_create_wiz.create({})
        with self.assertRaises(exceptions.Warning):
            wiz.do_create()
