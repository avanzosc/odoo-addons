# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common
from odoo.models import expression
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
from odoo.addons.calendar.models.calendar import calendar_id2real_id


@common.at_install(False)
@common.post_install(True)
class TestCalendarSurvey(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCalendarSurvey, cls).setUpClass()
        cls.action = cls.env.ref('survey.action_survey_user_input')
        cls.partner = cls.env.ref('base.partner_admin')
        cls.event_categ = cls.env.ref('calendar.categ_meet1')
        cls.survey = cls.env.ref('survey.feedback_form')
        cls.event_categ.write({
            'survey_ids': [(6, 0, cls.survey.ids)],
        })
        cls.event = cls.env['calendar.event'].create({
            'name': 'Test Event',
            'start': fields.Date.today(),
            'stop': fields.Date.today(),
            'allday': True,
            'partner_ids': [(6, 0, cls.partner.ids)],
            'categ_ids': [(6, 0, cls.event_categ.ids)],
        })
        cls.wizard_obj = cls.env['calendar.user_input']

    def test_calendar_survey(self):
        real_id = calendar_id2real_id(self.event.id)
        self.assertFalse(self.event.user_input_ids)
        wizard = self.wizard_obj.with_context({
            'active_id': self.event.id,
            'active_model': 'calendar.event'
        }).create({})
        self.assertEqual(self.event, wizard.event_id)
        self.assertIn(self.survey, wizard.survey_ids)
        self.assertIn(self.partner, wizard.partner_ids)
        wizard.create_survey_response()
        self.assertTrue(self.event.user_input_ids)
        self.assertEqual(
            self.event.user_input_count, len(self.event.user_input_ids))
        action_dict = self.event.button_open_user_input()
        domain = expression.AND([
            [('event_id', '=', real_id)],
            safe_eval(self.action.domain or '[]')])
        self.assertEquals(action_dict.get('domain'), domain)
        wizard = self.wizard_obj.with_context({
            'active_id': self.event.id,
            'active_model': 'calendar.event'
        }).create({
            'survey_ids': [],
            'partner_ids': [],
        })
        with self.assertRaises(UserError):
            wizard.create_survey_response()
