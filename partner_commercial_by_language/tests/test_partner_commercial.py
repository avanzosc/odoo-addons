# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestCommercialLanguage(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCommercialLanguage, cls).setUpClass()
        cls.ResPartner = cls.env["res.partner"]
        cls.ResUsers = cls.env['res.users']
        cls.ResLang = cls.env['res.lang']
        languages = cls.env['res.lang'].search([
            ['code', 'in', ['en_US', 'fr_FR']],
            '|', ['active', '=', True], ['active', '=', False]
        ])
        languages.write({'active': True})
        cls.lang_us = cls.ResLang.search([('code', '=', 'en_US')])
        cls.lang_fr = cls.ResLang.search([('code', '=', 'fr_FR')])
        cls.com_user_1 = cls.ResUsers.sudo().create({
            'name': 'Commercial User 1',
            'login': 'com_user1',
            'email': 'user1@example.com',
        })
        cls.com_user_2 = cls.ResUsers.sudo().create({
            'name': 'Commercial User 2',
            'login': 'com_user2',
            'email': 'user2@example.com',
        })

    def test_comercial_language(self):
        self.lang_us.commercial_user_id = self.com_user_1
        self.lang_us.commercial_user_id = self.com_user_2
        partner = self.ResPartner.create({"name": "Partner test", "lang": "en_US"})
        self.assertEqual(partner.user_id, self.com_user_1)
        partner.lang = self.lang_fr.code
        partner.onchange_lang()
        self.assertNotEqual(partner.user_id, self.lang_us.commercial_user_id)
