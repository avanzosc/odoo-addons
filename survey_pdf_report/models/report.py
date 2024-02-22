from odoo import fields, models, api, http
from odoo.http import request
from odoo.tools import format_datetime, format_date, is_html_empty
from odoo.addons.survey.controllers.main import Survey
from odoo.addons.survey.models.survey_user_input import SurveyUserInput

class Survey(Survey):

    def survey_print_report(self, survey_token, review=False, answer_token=None, **post):
        # Ensure proper use of action_print_answers_for_report on an instance
        user_input = self._get_user_input(survey_token, answer_token)
        report_data = user_input.action_print_answers_for_report()

        return {
            'is_html_empty': is_html_empty,
            'review': review,
            'survey': report_data.get('survey'),
            'answer': report_data.get('answer'),
            'questions_to_display': report_data.get('questions_to_display'),
            'scoring_display_correction': report_data.get('scoring_display_correction'),
            'format_datetime': lambda dt: format_datetime(request.env, dt, dt_format=False),
            'format_date': lambda date: format_date(request.env, date),
        }

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def action_print_answers_for_report(self):
        """ Open the website page with the survey form """
        self.ensure_one()
        survey_token = self.survey_id.access_token
        access_data = self._get_access_data(survey_token, ensure_token=False, check_partner=False)

        survey_sudo = access_data.get('survey_sudo')
        answer_sudo = access_data.get('answer_sudo')

        return {
            'survey': survey_sudo,
            'answer': answer_sudo,
            'questions_to_display': answer_sudo._get_print_questions() if answer_sudo else [],
            'scoring_display_correction': survey_sudo.scoring_type == 'scoring_with_answers' and answer_sudo,
        }


class SurveyUserInputReportData(models.AbstractModel):
    _name = 'report.survey_pdf_report.report_survey_pdf_custom_module'
    _description = 'Survey User Input Report Data'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        """ Generate report data based on the survey user input """
        # Ensure to handle docids properly, here assuming it's a list of ids
        user_inputs = self.env['survey.user_input'].browse(docids)
        
        # Use the data returned from action_print_answers_for_report
        report_data = user_inputs.mapped('action_print_answers_for_report')
        
        return {
            'is_html_empty': is_html_empty,
            'review': data.get('review', False),
            'survey': report_data[0].get('survey', False),
            'answer': report_data[0].get('answer', False),
            'questions_to_display': report_data[0].get('questions_to_display', []),
            'scoring_display_correction': report_data[0].get('scoring_display_correction', False),
            'format_datetime': lambda dt: format_datetime(request.env, dt, dt_format=False),
            'format_date': lambda date: format_date(request.env, date),
        }