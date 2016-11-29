# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.orgmichel fletcher/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleUtilities(common.TransactionCase):

    def setUp(self):
        super(TestSaleUtilities, self).setUp()
        self.partner_model = self.env['res.partner']
        self.env.ref('base.res_partner_address_4').write(
            {'ref': 'REF15252683',
             'vat': 'ES15252683A'})

    def test_sale_utilities(self):
        partners = self.partner_model.name_search('REF15252683')
        self.assertEqual(
            len(partners), 1, 'Partner not found by reference')
        partners = self.partner_model.name_search('ES15252683A')
        self.assertEqual(
            len(partners), 1, 'Partner not found by VAT')
