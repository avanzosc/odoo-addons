import logging
_logger = logging.getLogger(__name__)

from odoo import http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey

class Survey(Survey):
    http.route()
    def survey_display_page(self, survey_token, answer_token, **post):
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data, access_data['validity_code'])

        answer_sudo = access_data['answer_sudo']
        if answer_sudo.state != 'done' and answer_sudo.survey_time_limit_reached:
            answer_sudo._mark_done()

        # Filtrar los objetos de preguntas en survey_sudo
        filtered_questions = []
        for question in access_data['survey_sudo'].question_and_page_ids:
            if question and answer_sudo.inspected_building_id.service_start_date and any(
                normative.start_year <= int(answer_sudo.inspected_building_id.service_start_date.year) < normative.end_year 
                for normative in question.question_normative_ids
            ):
                filtered_questions.append(question.id) 

        # Actualizar question_and_page_ids de survey_sudo con los IDs de las preguntas filtradas
        access_data['survey_sudo'].question_and_page_ids = [(6, 0, filtered_questions)]

        # Log para registrar las preguntas filtradas
        filtered_question_titles = [request.env['survey.question'].browse(question_id).title for question_id in filtered_question_ids]
        _logger.info("2024okdeb - Preguntas filtradas en survey_sudo: %s", filtered_question_titles)

        return request.render('survey.survey_page_fill',
            self._prepare_survey_data(access_data['survey_sudo'], answer_sudo, **post))
