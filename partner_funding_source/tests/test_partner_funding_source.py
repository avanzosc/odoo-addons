# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestPartnerFundingSource(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPartnerFundingSource, cls).setUpClass()
        res_partner_model = cls.env['res.partner']
        funding_src_model = cls.env['funding.source']
        cls.partner = res_partner_model.create({
            'name': 'Test Partner',
        })
        cls.funding_src = funding_src_model.create({
            'name': 'Test Funding Source',
        })

    def test_computed_field_funding_source_count(self):
        self.assertFalse(self.partner.funding_source_ids)
        self.funding_src.partner_id = self.partner
        self.assertIn(self.funding_src, self.partner.funding_source_ids)
        self.assertTrue(self.partner.funding_source_count,
                        len(self.partner.funding_source_ids))
