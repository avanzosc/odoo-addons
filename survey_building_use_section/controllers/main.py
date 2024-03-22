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

        # Filtrar los IDs de las preguntas para obtener solo aquellos que cumplen con los criterios de tratamiento
        filtered_questions = []
        for question_id in answer_sudo.predefined_question_ids.ids:
            question = request.env['survey.question'].browse(question_id)
            if question and answer_sudo.inspected_building_id.service_start_date and any(
                normative.start_year <= int(answer_sudo.inspected_building_id.service_start_date.year) < normative.end_year 
                for normative in question.question_normative_ids
            ):
                filtered_questions.append(question)

        # Si no hay preguntas que pasen el filtro, mantén al menos una pregunta
        if not filtered_questions:
            filtered_questions = [answer_sudo.predefined_question_ids[0]]

        # Obtener los títulos de las preguntas filtradas
        filtered_question_titles = [question.title for question in filtered_questions]

        # Log para registrar los títulos de las preguntas filtradas
        _logger.info("2024okdeb - Preguntas filtradas: %s", filtered_question_titles)

        # Obtener los IDs de las preguntas filtradas
        filtered_question_ids = [question.id for question in filtered_questions]

        # Actualizar el campo predefined_question_ids del answer_sudo con los IDs filtrados
        answer_sudo.predefined_question_ids = [(6, 0, filtered_question_ids)]

        return request.render('survey.survey_page_fill',
            self._prepare_survey_data(access_data['survey_sudo'], answer_sudo, **post))
