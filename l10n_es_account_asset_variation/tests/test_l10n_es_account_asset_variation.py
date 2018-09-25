# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields


class TestL10nEsAccountAssetVariation(common.SavepointCase):

    def setUp(self):
        super(TestL10nEsAccountAssetVariation, self).setUp()
        self.asset_model = self.env['account.asset.asset']
        self.wiz_obj = self.env['account.asset.variation']
        self.ir_sequence_model = self.env['ir.sequence']
        self.sequence = self.env.ref(
            'l10n_es_account_asset_variation.account_asset_sequence')
        asset_vals = {
            'name': 'Test Variation Asset',
            'category_id': self.ref(
                'account_asset.account_asset_category_fixedassets0'),
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

    def test_asset_variation(self):
        self.asset.compute_depreciation_board()
        amount = (
            self.asset.purchase_value * (self.asset.method_percentage / 100))
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.amount != amount)
        self.assertFalse(lines, "The amount of lines is not correct.")
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage != self.asset.method_percentage)
        self.assertFalse(lines, "The percentage of lines is not correct.")
        new_percent = 5.0
        wiz_vals = {
            'start_date': fields.Date.from_string('2017-01-01'),
            'end_date': fields.Date.from_string('2018-01-01'),
            'percentage': new_percent,
        }
        wizard = self.wiz_obj.with_context(
            active_model='account.asset.asset', active_id=self.asset.id,
            active_ids=[self.asset.id]).create(wiz_vals)
        wizard.action_calculate_depreciation_board()
        self.assertEqual(
            sum(self.asset.mapped('depreciation_line_ids.amount')),
            self.asset.purchase_value)
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage == new_percent)
        self.assertEqual(len(lines), 1)
        amount = (
            self.asset.purchase_value * (new_percent / 100))
        self.assertEqual(sum(lines.mapped('amount')), amount)

    def test_asset_prorata_variation(self):
        self.asset.prorata = True
        self.asset.compute_depreciation_board()
        amount = (
            self.asset.purchase_value * (self.asset.method_percentage / 100))
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.amount != amount)
        self.assertFalse(lines, "The amount of lines is not correct.")
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage != self.asset.method_percentage)
        self.assertFalse(lines, "The percentage of lines is not correct.")
        new_percent = 5.0
        wiz_vals = {
            'start_date': fields.Date.from_string('2017-01-01'),
            'end_date': fields.Date.from_string('2018-01-01'),
            'percentage': new_percent,
        }
        wizard = self.wiz_obj.with_context(
            active_model='account.asset.asset', active_id=self.asset.id,
            active_ids=[self.asset.id]).create(wiz_vals)
        wizard.action_calculate_depreciation_board()
        self.assertEqual(
            sum(self.asset.mapped('depreciation_line_ids.amount')),
            self.asset.purchase_value)
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage == new_percent)
        self.assertEqual(len(lines), 1)
        amount = (
            self.asset.purchase_value * (new_percent / 100))
        self.assertEqual(sum(lines.mapped('amount')), amount)

    def test_asset_variation_number(self):
        self.asset.compute_depreciation_board()
        self.assertEqual(
            len(self.asset.depreciation_line_ids),
            (100 / self.asset.method_percentage))
        self.assertEqual(sum(
            self.asset.depreciation_line_ids.mapped('amount')),
            self.asset.purchase_value)
        self.assertEqual(sum(
            self.asset.depreciation_line_ids.mapped(
                'method_percentage')), 100)

    def test_new_asset_code_assign(self):
        code = self._get_next_code()
        asset = self.asset_model.create({
            'name': 'Testing asset code',
            'purchase_value': 1000,
            'category_id': self.ref(
                'account_asset.account_asset_category_fixedassets0'),
        })
        self.assertNotEqual(asset.sequence, '/')
        self.assertEqual(asset.sequence, code)

    def test_copy_asset_code_assign(self):
        code = self._get_next_code()
        asset_copy = self.asset.copy()
        self.assertNotEqual(asset_copy.sequence, self.asset.sequence)
        self.assertEqual(asset_copy.sequence, code)

    def _get_next_code(self):
        d = self.ir_sequence_model._interpolation_dict()
        prefix = self.ir_sequence_model._interpolate(
            self.sequence.prefix, d)
        suffix = self.ir_sequence_model._interpolate(
            self.sequence.suffix, d)
        code = (prefix + ('%%0%sd' % self.sequence.padding %
                          self.sequence.number_next_actual) + suffix)
        return code
