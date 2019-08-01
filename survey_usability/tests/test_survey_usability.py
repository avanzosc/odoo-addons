# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSurveyUsability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSurveyUsability, cls).setUpClass()
        cls.survey = cls.env.ref('survey.feedback_form')
        cls.response = cls.env['survey.user_input'].create({
            'survey_id': cls.survey.id,
            'type': 'manually',
        })

    def test_survey_usability(self):
        action_dict = self.response.button_respond_survey()
        self.assertEquals(action_dict.get('type'), 'ir.actions.act_url')
