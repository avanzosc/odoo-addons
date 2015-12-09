# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestCrmClaimFilter(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimFilter, self).setUp()
        self.claim_model = self.env['crm.claim']
        self.partner_model = self.env['res.partner']
        self.partner = self.env.ref('base.res_partner_2')
        self.partner.write({'vat': 'ESA12345674',
                            'mobile': '943943943'})

    def test_crm_claim_filter(self):
        vals = {'name': 'Testing module',
                'partner_id': self.partner.id}
        claim = self.claim_model.create(vals)
        self.assertEqual(
            claim.vat, self.partner.vat,
            'VAT of the claim, does not match with partner vat')
        self.assertEqual(
            claim.mobile, self.partner.mobile,
            'VAT of the claim, does not match with partner vat')

    def test_crm_claim_filter_partner_search(self):
        partners = self.partner_model.name_search(
            name='ESA12345674', args=None)
        self.assertNotEqual(
            len(partners), 0, 'Partner was not found when searching for vat')
