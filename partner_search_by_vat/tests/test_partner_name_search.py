# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import openerp.tests.common as common


class TestPartnerNameSearch(common.TransactionCase):
    def setUp(self):
        super(TestPartnerNameSearch, self).setUp()
        self.product_name = 'StockQuantTestProduct'
        self.uom = self.browse_ref('product.product_uom_dozen')
        self.partner_model = self.env['res.partner'].sudo()
        self.vat_code = 'ES12345678Z'
        self.partner1 = self.env['res.partner'].create({
            'name': 'Test Partner',
            'vat': 'ES12345678Z',
            })
        self.partner2 = self.env['res.partner'].create({
            'name': 'Test Partner2',
        })

    def test_partner_name_search(self):
        res_search = self.partner_model.name_search(name=self.vat_code)
        partner_ids = map(lambda x: x[0], res_search)
        self.assertNotEqual(
            len(res_search), 0, 'There must be at least one partner created.')
        self.assertEqual(
            len(res_search), 1, 'There must be only one partner created.')
        self.assertIn(self.partner1.id, partner_ids)
        self.assertNotIn(self.partner2.id, partner_ids)
