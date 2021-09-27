# Copyright 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestNameCodeYearId(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestNameCodeYearId, cls).setUpClass()
        cls.event_obj = cls.env['event.event']
        cls.skill_type_lang = cls.env.ref('hr_skills.hr_skill_type_lang')
        cls.skill_spanish = cls.env.ref('hr_skills.hr_skill_spanish')
        cls.skill_filipino = cls.env.ref('hr_skills.hr_skill_filipino')
        cls.skill_type_lang.skill_language = True
        cls.skill_spanish.code = 'SP'
        cls.skill_filipino.code = 'FI'

    def test_event_name_code_year_id(self):
        vals = {'name': 'User for event lang level',
                'date_begin': '2025-01-06 08:00:00',
                'date_end': '2025-01-15 10:00:00',
                'lang_id': self.skill_spanish.id}
        event = self.event_obj.create(vals)
        name = 'SP-{}-2025'.format(event.id)
        self.assertEqual(event.name, name)
        vals = {'date_begin': '2024-01-06 08:00:00',
                'lang_id': self.skill_filipino.id}
        event.write(vals)
        name = 'FI-{}-2024'.format(event.id)
        self.assertEqual(event.name, name)
