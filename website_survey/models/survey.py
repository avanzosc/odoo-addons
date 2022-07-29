
from odoo import api, fields, models
import werkzeug


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        url = '/my/survey/'+str(self.id)
        return url
