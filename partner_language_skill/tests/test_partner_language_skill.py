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
