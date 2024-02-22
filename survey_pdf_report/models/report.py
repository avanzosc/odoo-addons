from odoo import fields, models, api, http
from odoo.http import request
from odoo.tools import format_datetime, format_date, is_html_empty
from odoo.addons.survey.controllers.main import Survey
from odoo.addons.survey.models.survey_user_input import SurveyUserInput

import requests
import json

class Survey(Survey):
    @http.route('/survey/print/pdf_report/<string:survey_token>', type='json', auth='public', website=True, sitemap=False)
    def survey_print(self, survey_token, review=False, answer_token=None, **post):
        '''Display a survey in printable view; if <answer_token> is set, it will
        grab the answers of the user_input_id that has <answer_token>.'''
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=False, check_partner=False)
        if access_data['validity_code'] is not True and (
                access_data['has_survey_access'] or
                access_data['validity_code'] not in ['token_required', 'survey_closed', 'survey_void']):
            return self._redirect_with_error(access_data, access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']
        context = {
            'is_html_empty': is_html_empty,
            'review': review,
            'survey': survey_sudo,
            'answer': answer_sudo if survey_sudo.scoring_type != 'scoring_without_answers' else answer_sudo.browse(),
            'questions_to_display': answer_sudo._get_print_questions(),
            'scoring_display_correction': survey_sudo.scoring_type == 'scoring_with_answers' and answer_sudo,
            'format_datetime': lambda dt: format_datetime(request.env, dt, dt_format=False),
            'format_date': lambda date: format_date(request.env, date),
        }
        return context



class SurveyUserInputReportData(models.AbstractModel):
    _name = 'report.survey_pdf_report.report_survey_pdf_custom_module'
    _description = 'Survey User Input Report Data'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        user_inputs = self.env['survey.user_input'].browse(docids)
        report_data = []

        for user_input in user_inputs:
            # Construye la URL completa para la solicitud HTTP
            url = f'{base_url}/survey/print/pdf_report/{user_input.survey_id.access_token}?answer_token={user_input.access_token}'
            
            # Realiza la solicitud HTTP para obtener los valores
            response = requests.get(url)
            
            # Procesa la respuesta según tu formato esperado
            try:
                response.raise_for_status()
                survey_data = response.json()  # Aquí utilizamos .json() en lugar de .text
                report_data.append(survey_data)
            except requests.exceptions.HTTPError as errh:
                report_data.append({'error': f'HTTP Error: {errh}'})
            except requests.exceptions.ConnectionError as errc:
                report_data.append({'error': f'Error de conexión: {errc}'})
            except requests.exceptions.Timeout as errt:
                report_data.append({'error': f'Tiempo de espera agotado: {errt}'})
            except requests.exceptions.RequestException as err:
                report_data.append({'error': f'Error en la solicitud HTTP: {err}'})
        
        # Utiliza el último valor de survey_data
        last_survey_data = report_data[-1] if report_data else {}
        print("\n\n",report_data)
        # Construye el diccionario JSON
        json_data = {
            'is_html_empty': is_html_empty,
            'review': data.get('review', False),
            'survey': last_survey_data.get('survey', False),
            'answer': last_survey_data.get('answer', False),
            'questions_to_display': last_survey_data.get('questions_to_display', []),
            'scoring_display_correction': last_survey_data.get('scoring_display_correction', False),
            'format_datetime': lambda dt: format_datetime(self.env, dt, dt_format=False),
            'format_date': lambda date: format_date(self.env, date),
        }

        return json_data
