# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import AccountBankingMandateUsabilityCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestAccountBankingMandateUsability(AccountBankingMandateUsabilityCommon):

    def test_generate_banking_mandate(self):
        self.assertFalse(self.bank.mandate_ids)
        self.bank.generate_account_banking_mandate()
        self.assertTrue(self.bank.mandate_ids)
