# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields


class TestL10nEsAccountAssetVariation(common.TransactionCase):

    def setUp(self):
        super(TestL10nEsAccountAssetVariation, self).setUp()
        self.asset_model = self.env['account.asset.asset']
        self.wiz_obj = self.env['account.asset.variation']
        asset_vals = {
            'name': 'Test Variation Asset',
            'category_id': self.ref('account_asset.account_asset_category_'
                                    'fixedassets0'),
            'code': 'REF01',
            'purchase_date': fields.Date.from_string('2015-01-01'),
            'method': 'linear',
            'purchase_value': 30000,
            'method_time': 'percentage',
            'move_end_period': True,
            'method_number': 10,
            'method_percentage': 10,
            'method_period': 12
            }
        self.asset = self.asset_model.create(asset_vals)
        asset_vals = {
            'name': 'Test Variation Asset',
            'category_id': self.ref('account_asset.account_asset_category_'
                                    'fixedassets0'),
            'code': 'REF02',
            'purchase_date': fields.Date.from_string('2015-01-01'),
            'method': 'linear',
            'purchase_value': 500,
            'method_time': 'percentage',
            'move_end_period': True,
            'method_number': 20,
            'method_percentage': 20,
            'method_period': 12
            }
        self.asset2 = self.asset_model.create(asset_vals)
        asset_vals = {
            'name': 'Test Variation Asset 3',
            'category_id': self.ref('account_asset.account_asset_category_'
                                    'fixedassets0'),
            'code': 'REF03',
            'purchase_date': fields.Date.from_string('2015-01-01'),
            'method': 'linear',
            'purchase_value': 500,
            'method_time': 'number',
            'move_end_period': True,
            'method_number': 3,
            'method_period': 12,
            }
        self.asset3 = self.asset_model.create(asset_vals)

    def test_asset_variation(self):
        self.asset.compute_depreciation_board()
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.amount != 3000)
        self.assertFalse(lines, "The amount of lines is not correct.")
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage != 10)
        self.assertFalse(lines, "The percentage of lines is not correct.")
        wiz_vals = {
            'start_date': fields.Date.from_string('2017-01-01'),
            'end_date': fields.Date.from_string('2018-01-01'),
            'percentage': 5,
            }
        wizard = self.wiz_obj.with_context(
            active_model='account.asset.asset', active_id=self.asset.id,
            active_ids=[self.asset.id]).create(wiz_vals)
        wizard.action_calculate_depreciation_board()
        self.assertEqual(
            sum(self.asset.depreciation_line_ids.mapped('amount')), 30000)
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage == 5)
        self.assertEqual(len(lines), 2)
        amount = sum(lines.mapped('amount'))
        self.assertEqual(amount, 3000)

    def test_asset_variation2(self):
        self.asset2.compute_depreciation_board()
        lines = self.asset2.depreciation_line_ids.filtered(
            lambda x: x.amount != 100)
        self.assertFalse(lines, "The amount of lines is not correct.")
        lines = self.asset2.depreciation_line_ids.filtered(
            lambda x: x.method_percentage != 20)
        self.assertFalse(lines, "The percentage of lines is not correct.")
        wiz_vals = {
            'start_date': fields.Date.from_string('2017-12-31'),
            'end_date': fields.Date.from_string('2017-12-31'),
            'percentage': 6,
            }
        wizard = self.wiz_obj.with_context(
            active_model='account.asset.asset', active_id=self.asset2.id,
            active_ids=[self.asset2.id]).create(wiz_vals)
        wizard.action_calculate_depreciation_board()
        self.assertEqual(
            sum(self.asset2.depreciation_line_ids.mapped('amount')), 530)
        line = self.asset2.depreciation_line_ids.filtered(
            lambda x: x.method_percentage == 6)
        self.assertEqual(len(line), 1)
        self.assertEqual(line.amount, 30.0)
        self.assertEqual(len(self.asset2.depreciation_line_ids), 6)
        self.asset2.prorata = True
        self.asset2.depreciation_line_ids[0].move_id = 1
        result = self.asset2._get_last_depreciation_date()
        self.assertEqual(result.get(self.asset2.id), '2016-12-31')
        self.asset2.with_context(wiz=wizard)._compute_board_amount(
            self.asset2, 1, 2, 4, 5, [], 6,
            fields.Date.from_string('2016-12-31'))
        self.asset2.method_period = 1
        result = self.asset2.with_context(wiz=wizard)._compute_board_amount(
            self.asset2, 1, 2, 4, 5, [], 6,
            fields.Date.from_string('2016-12-31'))
        self.assertEqual(round(result, 2), 3.23)

    def test_asset_variation_number(self):
        self.asset3.compute_depreciation_board()
        self.assertEqual(len(self.asset3.depreciation_line_ids), 4)
        self.assertEqual(sum(
            self.asset3.depreciation_line_ids.mapped('amount')), 500)
        self.assertEqual(sum(
            self.asset3.depreciation_line_ids.mapped(
                'method_percentage')), 100)

    def test_asset_copy(self):
        asset4 = self.asset3.copy()
        self.assertNotEqual(self.asset3.sequence, asset4.sequence)
