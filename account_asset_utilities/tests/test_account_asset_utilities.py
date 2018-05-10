# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.account_asset.tests.test_account_asset import TestAccountAsset
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class TestAccountAssetUtilities(TestAccountAsset):

    def setUp(self):
        super(TestAccountAssetUtilities, self).setUp()
        self._load('account', 'test', 'account_minimal_test.xml')
        self._load('account_asset', 'test', 'account_asset_demo_test.xml')
        asset_category = self.browse_ref(
            'account_asset.account_asset_category_fixedassets_test0')

        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        product = self.env['product.product'].create({
            'name': 'Test Product',
        })

        # Should be changed by automatic on_change later
        invoice_account = self.env['account.account'].search(
            [('user_type_id', '=',
              self.env.ref('account.data_account_type_receivable').id)],
            limit=1).id
        invoice_line_account = self.env['account.account'].search(
            [('user_type_id', '=',
              self.env.ref('account.data_account_type_expenses').id)],
            limit=1).id

        self.invoice = self.env['account.invoice'].create({
            'partner_id': partner.id,
            'account_id': invoice_account,
            'type': 'in_invoice',
        })

        self.invoice_line = self.env['account.invoice.line'].create({
            'product_id': product.id,
            'quantity': 1.0,
            'price_unit': 100.0,
            'invoice_id': self.invoice.id,
            'name': 'product that cost 100',
            'account_id': invoice_line_account,
            'asset_category_id': asset_category.id,
        })

    def test_account_asset_utilities(self):
        self.assertFalse(self.invoice_line.account_asset_ids)
        result = self.invoice.show_assets_from_invoice()
        self.assertEquals(result, {})
        self.invoice.action_move_create()
        self.invoice.invalidate_cache()
        self.assertTrue(self.invoice_line.account_asset_ids)
        self.assertEquals(
            self.invoice.assets_count,
            len(self.invoice.mapped('invoice_line_ids.account_asset_ids')))
        result = self.invoice.show_assets_from_invoice()
        action = self.env.ref(
            'account_asset.action_account_asset_asset_form')
        action_dict = action.read()[0] if action else {}
        new_domain = [('invoice_id', '=', self.invoice.id)]
        action_domain = expression.AND(
            [new_domain, safe_eval(action_dict.get('domain') or '[]')])
        domain = result.get('domain')
        self.assertEquals(action_domain, domain)
