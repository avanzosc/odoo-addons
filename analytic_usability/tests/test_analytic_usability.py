# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestAnalyticUsability(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account = cls.env.ref("analytic.analytic_administratif")
        cls.line = cls.env["account.analytic.line"].create(
            {
                "name": "Test Line",
                "account_id": cls.account.id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "user_id": cls.env.ref("base.user_admin").id,
            }
        )

    def test_analytic_usability(self):
        self.assertEqual(self.line.amount, 0)
        self.assertEqual(self.line.amount_type, "cost")
        self.line.write(
            {
                "amount": -100,
            }
        )
        self.assertEqual(self.line.amount_type, "cost")
        self.line.write(
            {
                "amount": 100,
            }
        )
        self.assertEqual(self.line.amount_type, "revenue")

    def test_analytic_account(self):
        self.assertFalse(self.account.partner_id)
        self.assertEqual(self.account.user_id, self.env.user)
        self.account.write(
            {
                "partner_id": self.partner.id,
            }
        )
        self.account._onchange_partner_id()
        self.assertEqual(self.account.user_id, self.partner.user_id)
