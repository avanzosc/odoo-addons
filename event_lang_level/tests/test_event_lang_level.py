# Copyright 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEventLangLevel(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventLangLevel, cls).setUpClass()
        cls.user_obj = cls.env['res.users']
        cls.employee_skill_obj = cls.env['hr.employee.skill']
        cls.skill_type_lang = cls.env.ref('hr_skills.hr_skill_type_lang')
        cls.skill_spanish = cls.env.ref('hr_skills.hr_skill_spanish')
        cls.skill_filipino = cls.env.ref('hr_skills.hr_skill_filipino')
        cls.skill_level = cls.env.ref('hr_skills.hr_skill_level_c2')
        cls.employee = cls.env.ref("hr.employee_hne")
        cls.event = cls.env.ref("event.event_7")

    def test_event_lang_level(self):
        vals = {'name': 'User for event lang level',
                'login': 'eventlanglevel@avanzosc.es'}
        user = self.user_obj.create(vals)
        self.skill_type_lang.skill_language = True
        self.employee.user_id = user.id
        self.assertEqual(len(user.lang_ids), 1)
        self.assertEqual(len(user.partner_id.lang_ids), 1)
        self.event.write({'lang_id': self.skill_spanish.id,
                          'level_id': self.skill_level.id})
        for track in self.event.track_ids:
            self.assertEqual(track.lang_id, self.skill_spanish)
            self.assertEqual(track.level_id, self.skill_level)
        vals = {'employee_id': self.employee.id,
                'skill_id': self.skill_filipino.id,
                'skill_type_id': self.skill_filipino.skill_type_id.id,
                'skill_level_id': self.skill_level.id}
        self.employee_skill_obj.create(vals)
        self.assertEqual(len(user.lang_ids), 2)
        self.assertEqual(len(user.partner_id.lang_ids), 2)
