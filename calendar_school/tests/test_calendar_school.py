# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestCalendarSchoolCommon
from odoo.tests import common
from odoo.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class TestCalendarSchool(TestCalendarSchoolCommon):

    def test_calendar_school(self):
        self.assertEquals(self.student.student_count_meetings, 0)
        self.assertEquals(self.family.family_count_meetings, 0)
        self.assertEquals(self.teacher.count_meetings, 0)
        self.assertEquals(self.tutor.count_meetings, 0)
        self.tutor.generate_meetings()
        self.tutor.invalidate_cache()
        self.assertEquals(self.student.student_count_meetings, 4)
        action_dict = self.student.button_show_meetings()
        self.assertIn(
            ('student_id', 'in', self.student.ids),
            action_dict.get('domain'))
        self.assertEquals(self.family.family_count_meetings, 2)
        action_dict = self.family.button_show_meetings()
        self.assertIn(
            ('family_id', 'in', self.family.ids),
            action_dict.get('domain'))
        self.assertEquals(self.teacher.count_meetings, 4)
        action_dict = self.teacher.button_show_meetings()
        self.assertIn(
            ('teacher_id', 'in', self.teacher.ids),
            action_dict.get('domain'))
        self.assertEquals(self.tutor.count_meetings, 4)
        action_dict = self.tutor.button_show_meetings()
        self.assertIn(
            ('supervised_year_id', 'in', self.tutor.ids),
            action_dict.get('domain'))
        event = self.tutor.meeting_ids[:1]
        self.assertEquals(event.state, 'draft')
        event.action_open()
        self.assertEquals(event.state, 'open')
        self.assertFalse(event.description)
        with self.assertRaises(ValidationError):
            event.action_done()
        event.description = 'Test Description'
        event.action_done()
        self.assertEquals(event.state, 'done')
        event.action_cancel()
        self.assertEquals(event.state, 'cancel')
        event.action_draft()
        self.assertEquals(event.state, 'draft')

    def test_calendar_school_wizard(self):
        self.assertEquals(self.tutor.count_meetings, 0)
        wiz = self.wizard_model.with_context(
            active_ids=self.tutor.ids).create({})
        wiz.meetings_confirm()
        self.tutor.invalidate_cache()
        self.assertEquals(self.tutor.count_meetings, 4)
