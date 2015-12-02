# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestCrmClaimCategParent(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimCategParent, self).setUp()
        self.categ_model = self.env['crm.case.categ']
        self.claim_model = self.env['crm.claim']
        vals = {'name': 'My parent category'}
        self.categ_parent = self.categ_model.create(vals)
        self.categ = self.browse_ref('crm_claim.categ_claim1')
        self.categ.parent_id = self.categ_parent.id

    def test_crm_claim_filter(self):
        vals = {'name': 'Testing module',
                'categ_id': self.categ.id}
        claim = self.claim_model.create(vals)
        claim.onchange_categ_id()
        self.assertEqual(
            claim.categ_id.section_id.id, claim.section_id.id,
            'Section claim, not equal to section category.')
