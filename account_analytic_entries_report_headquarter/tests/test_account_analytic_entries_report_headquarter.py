# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestAccountAnalyticEntriesReportHeadquarter(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticEntriesReportHeadquarter, self).setUp()
        self.headquarter = self.env['res.headquarters'].create(
            {'code': 'testheadquarter', 'name': 'Test headquarter'})
        self.product_category = self.env['product.category'].create(
            {'name': 'Product category for headquarter',
             'type': 'normal'})
        self.product = self.env['product.product'].create(
            {'name': 'Product for headquarter',
             'sale_ok': True,
             'type': 'consu',
             'categ_id': self.product_category.id})
        self.partner = self.env['res.partner'].create(
            {'name': 'Partner for headquarter',
             'customer': True,
             'headquarters_id': self.headquarter.id})
        self.account_type = self.env['account.account.type'].create(
            {'name': 'Type account for headquarter',
             'code': 'ACCOUNT-HEADQURTEER-TYPE'})
        self.account = self.env['account.account'].create(
            {'code': 'ACCOUNT-HEADQUARTER',
             'name': 'Account for headquarter',
             'type': 'other',
             'user_type': self.account_type.id})
        self.analytic_account = self.env['account.analytic.account'].create(
            {'name': 'Account analytic account for headquarter',
             'type': 'normal',
             'code': 'HEADQUARTER',
             'partner_id': self.partner.id})
        self.analytic_journal = self.env['account.analytic.journal'].create(
            {'name': 'Journal for headquarter',
             'type': 'general'})
        self.analytic_line = self.env['account.analytic.line'].create(
            {'name': 'Analytic line for headquarter',
             'account_id': self.analytic_account.id,
             'general_account_id': self.account.id,
             'journal_id': self.analytic_journal.id,
             'product_id': self.product.id,
             'product_categ_id': self.product_category.id,
             'headquarters_id': self.headquarter.id,
             'product_uom_id': self.product.uom_id.id,
             'amount': 5,
             'unit_amount': 30})

    def test_account_analytic_entries_report_headquarter(self):
        cond = [('product_id', '=', self.product.id)]
        report = self.env['analytic.entries.report'].search(cond)
        self.assertEqual(
            report.headquarters_id.id, self.headquarter.id,
            'Bad headquarter for report.')
        self.assertEqual(
            report.product_categ_id.id, self.product_category.id,
            'Bad product category for report.')
