# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestCrmClaimTeam(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimTeam, self).setUp()
        self.case_section_obj = self.env['crm.case.section']
        self.stage1 = self.env.ref('crm_claim.stage_claim1')
        self.stage2 = self.env.ref('crm_claim.stage_claim2')
        self.stage3 = self.env.ref('crm_claim.stage_claim3')
        self.stage4 = self.env.ref('crm_claim.stage_claim5')

    def test_crm_claim_team_default_stage(self):
        self.stage1.case_default = False
        self.stage2.case_default = False
        self.stage3.case_default = True
        self.stage4.case_default = True
        self.case_section = self.case_section_obj.create(
            {'name': 'Claim1'})
        self.assertEqual(2, len(self.case_section.claim_stage_ids),
                         'Not the same number of stages')
