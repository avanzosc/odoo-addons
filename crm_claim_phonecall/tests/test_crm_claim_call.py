# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestCrmClaimCall(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimCall, self).setUp()
        self.crm_claim = self.env.ref('crm_claim.crm_claim_1')
        self.phonecall1 = self.env.ref('crm.crm_phonecall_1')

    def test_crm_claim(self):
        phonecalls = [(6, 0, [self.phonecall1.id])]
        self.crm_claim.phonecall_ids = phonecalls
        self.assertEqual(
            self.crm_claim.phonecalls_count, len(self.crm_claim.phonecall_ids),
            'Should be 1 phonecall')
