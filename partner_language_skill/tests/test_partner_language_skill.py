# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestPartnerLanguageSkill(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPartnerLanguageSkill, cls).setUpClass()
        cls.skill_model = cls.env['res.lang.skill']
        cls.wiz_model = cls.env['res.partner.lang.skill.creator']
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })
        cls.skill = cls.skill_model.create({
            'name': 'First Certificate in English (FCE)',
            'level': 'B2',
            'lang_id': cls.env.ref('base.lang_en').id,
        })

    def test_lang_skill_name(self):
        self.skill.invalidate_cache()
        self.assertEqual(
            self.skill.display_name,
            '{} - {} - {}'.format(
                self.skill.level, self.skill.name, self.skill.lang_id.name))

    def test_partner_lang_wizard(self):
        self.assertFalse(self.partner.lang_skill_ids)
        wizard = self.wiz_model.with_context(
            active_model=self.partner._name,
            active_ids=self.partner.ids).create({
                'lang_id': self.skill.id,
            })
        wizard.button_create_skills()
        self.assertTrue(self.partner.lang_skill_ids)
        self.assertFalse(any(self.partner.mapped('lang_skill_ids.obtained')))
        self.partner.lang_skill_ids.button_mark_obtained()
        self.assertTrue(any(self.partner.mapped('lang_skill_ids.obtained')))
