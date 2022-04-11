# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestCommercialLanguage(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCommercialLanguage, cls).setUpClass()
        cls.ResPartner = cls.env["res.partner"]
        cls.ResUsers = cls.env["res.users"]
        cls.ResLang = cls.env["res.lang"]
        cls.CrmTeam = cls.env["crm.team"]
        languages = cls.env["res.lang"].search([
            ["code", "in", ["en_US", "fr_FR"]],
            "|", ["active", "=", True], ["active", "=", False]
        ])
        languages.write({"active": True})
        cls.lang_us = cls.ResLang.search([("code", "=", "en_US")])
        cls.lang_fr = cls.ResLang.search([("code", "=", "fr_FR")])
        cls.com_user_1 = cls.ResUsers.sudo().create({
            "name": "Commercial User 1",
            "login": "com_user1",
            "email": "user1@example.com",
            "commercial_lang_ids": [(4, cls.lang_us.id), (4, cls.lang_fr.id)],
        })
        cls.com_user_2 = cls.ResUsers.sudo().create({
            "name": "Commercial User 2",
            "login": "com_user2",
            "email": "user2@example.com",
            "commercial_lang_ids": [(4, cls.lang_us.id), (4, cls.lang_fr.id)],
        })
        cls.sales_team = cls.CrmTeam.sudo().create({
            "name": "Test Sales Team",
            "sequence": 5,
            "member_ids": [(4, cls.com_user_1.id), (4, cls.com_user_2.id)],
        })

    def test_comercial_language(self):
        partner_1 = self.ResPartner.create({"name": "Partner 1 test", "lang": "en_US"})
        self.assertEqual(partner_1.user_id, self.com_user_1)
        partner_2 = self.ResPartner.create({"name": "Partner 2 test", "lang": "en_US"})
        self.assertEqual(partner_2.user_id, self.com_user_2)
