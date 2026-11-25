# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):
    def test_company_id_defaults_to_current_company(self):
        partner = self.env["res.partner"].create(
            {"name": "Test contact company default"}
        )

        self.assertEqual(partner.company_id, self.env.company)
