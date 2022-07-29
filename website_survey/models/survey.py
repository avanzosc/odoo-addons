
from odoo import api, fields, models
import werkzeug


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        url = '/my/survey/'+str(self.id)
        return url

    def action_print_certification(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        """ Open the website page with the survey form """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "View Answers",
            'target': 'self',
            'url': '/survey/certification/print/%s?answer_token=%s' % (
                self.survey_id.access_token, self.access_token)
        }
