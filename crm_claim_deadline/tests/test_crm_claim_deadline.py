# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestCrmClaimDeadline(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimDeadline, self).setUp()
        self.claim_model = self.env['crm.claim']
        self.partner_model = self.env['res.partner']
        self.partner = self.env.ref('base.res_partner_2')
        self.company = self.env.ref('base.main_company')
        self.company.write({'claim_closing_days': 5})

    def test_crm_claim_deadline(self):
        vals = {'name': 'Testing module',
                'partner_id': self.partner.id}
        claim = self.claim_model.create(vals)
        self.assertNotEqual(
            claim.date_deadline, False, 'Claim Deadline no generated')
