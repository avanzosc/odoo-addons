# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestMaintenanceEquipmentExtraInfoAsset(common.TransactionCase):

    def setUp(self):
        super(TestMaintenanceEquipmentExtraInfoAsset, self).setUp()
        self.account_obj = self.env['account.account']
        self.account_type_obj = self.env['account.account.type']
        self.asset_obj = self.env['account.asset.asset']
        self.account_type = self.account_type_obj.create(
            {'name': 'Account type for extra info asset',
             'include_initial_balance': True,
             'type': 'other'})
        account_vals = {'name': 'Account for test extra info asset',
                        'code': 100001,
                        'display_name': 'Account for test extra info asset',
                        'user_type_id': self.account_type.id}
        self.account = self.account_obj.create(account_vals)
        self.account_type = self.account_type_obj.create(
            {'name': 'Account expense type for extra info asset',
             'include_initial_balance': False,
             'type': 'other'})
        account_expense_vals = {
            'name': 'Account expense for test extra info asset',
            'code': 211001,
            'display_name': 'Account expense for test extra info asset',
            'user_type_id': self.account_type.id}
        self.account_expense = self.account_obj.create(account_expense_vals)
        journal_vals = {'name': 'Journal for test extra info asset',
                        'type': 'general',
                        'code': 'AAA',
                        'sequence_number_next': 1}
        self.journal = self.env['account.journal'].create(journal_vals)
        asset_category_vals = {
            'name': 'Asset category',
            'method': 'linear',
            'method_time': 'number',
            'method_number': 3,
            'method_period': 1,
            'method_progress_factor': 0.3,
            'type': 'purchase',
            'account_asset_id': self.account.id,
            'account_depreciation_id': self.account.id,
            'account_depreciation_expense_id': self.account_expense.id,
            'journal_id': self.journal.id}
        self.asset_category = self.env['account.asset.category'].create(
            asset_category_vals)
        cond = [('name', '=', 'Account Payable')]
        self.account = self.env['account.account'].search(cond)
        cond = [('name', '=', 'Fixed Asset Account')]
        self.account2 = self.env['account.account'].search(cond)
        invoice_line_vals = {
            'product_id': self.ref('product.product_delivery_02'),
            'name': 'Invoice line equipment invoice assset',
            'account_id': self.account2.id,
            'quantity': 1,
            'price_unit': 25.0,
            'asset_category_id': self.asset_category.id}
        invoice_vals = {
            'name': 'Invoice equipment invoice line asset',
            'partner_id': self.ref('base.res_partner_1'),
            'account_id': self.account.id,
            'type': 'in_invoice',
            'invoice_line_ids': [(0, 0, invoice_line_vals)]}
        self.invoice = self.env['account.invoice'].create(invoice_vals)

    def test_maintenance_equipment_extra_info_asset(self):
        self.invoice.action_invoice_open()
        self.assertEqual(
            self.invoice.assets_count, 1, 'BAD assets count for invoice')
        cond = [('invoice_line_id', '=', self.invoice.invoice_line_ids[0].id)]
        asset = self.asset_obj.search(cond)
        result = self.invoice.show_assets_from_invoice()
        domain = "[('id', 'in', [{}])]".format(asset.id)
        self.assertEqual(
            str(result.get('domain')), domain, 'BAD domain from invoice')
