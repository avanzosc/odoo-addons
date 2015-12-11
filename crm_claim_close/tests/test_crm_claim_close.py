# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestCrmClaimClose(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimClose, self).setUp()
        self.crm_claim = self.env.ref('crm_claim.crm_claim_1')

    def test_crm_claim(self):
        self.crm_claim.claim_close()
        self.assertNotEqual(self.crm_claim.date_closed, False, 'The claim has'
                            ' not been closed')
        self.crm_claim.claim_re_open()
        self.assertEqual(self.crm_claim.date_closed, False, 'The claim has not'
                         ' been opened')
        self.assertEqual(self.crm_claim.stage_id.id,
                         self.crm_claim._get_default_stage_id(),
                         'The stage is not correct')
