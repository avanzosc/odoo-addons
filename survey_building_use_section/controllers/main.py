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

        return request.render('survey.survey_page_fill',
            self._prepare_survey_data(access_data['survey_sudo'], answer_sudo, **post))
        
        
        
    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        """ Survey page navigation is done in AJAX. This function prepare the 'next page' to display in html
        and send back this html to the survey_form widget that will inject it into the page.
        Background url must be given to the caller in order to process its refresh as we don't have the next question
        object at frontend side."""
        survey_data = self._prepare_survey_data(survey_sudo, answer_sudo, **post)

        _logger.info("2024okdeb - Contenido de survey_data: %s", survey_data)
        
        _logger.info("2024okdeb - Contenido detallado de survey_data:")
        if 'is_html_empty' in survey_data:
            _logger.info("2024okdeb - is_html_empty: %s", survey_data['is_html_empty'])
        if 'survey' in survey_data:
            _logger.info("2024okdeb - survey: %s", survey_data['survey'])
        if 'answer' in survey_data:
            _logger.info("2024okdeb - answer: %s", survey_data['answer'])
        if 'breadcrumb_pages' in survey_data:
            _logger.info("2024okdeb - breadcrumb_pages: %s", survey_data['breadcrumb_pages'])
        if 'format_datetime' in survey_data:
            _logger.info("2024okdeb - format_datetime: %s", survey_data['format_datetime'])
        if 'format_date' in survey_data:
            _logger.info("2024okdeb - format_date: %s", survey_data['format_date'])
        if 'triggering_answer_by_question' in survey_data:
            _logger.info("2024okdeb - triggering_answer_by_question: %s", survey_data['triggering_answer_by_question'])
        if 'triggered_questions_by_answer' in survey_data:
            _logger.info("2024okdeb - triggered_questions_by_answer: %s", survey_data['triggered_questions_by_answer'])
        if 'selected_answers' in survey_data:
            _logger.info("2024okdeb - selected_answers: %s", survey_data['selected_answers'])
        if 'survey_last' in survey_data:
            _logger.info("2024okdeb - survey_last: %s", survey_data['survey_last'])
        if 'page' in survey_data:
            _logger.info("2024okdeb - page: %s", survey_data['page'])
        if 'has_answered' in survey_data:
            _logger.info("2024okdeb - has_answered: %s", survey_data['has_answered'])
        if 'can_go_back' in survey_data:
            _logger.info("2024okdeb - can_go_back: %s", survey_data['can_go_back'])
        if 'previous_page_id' in survey_data:
            _logger.info("2024okdeb - previous_page_id: %s", survey_data['previous_page_id'])

        if answer_sudo.state == 'done':
            survey_content = request.env['ir.qweb']._render('survey.survey_fill_form_done', survey_data)
        else:
            survey_content = request.env['ir.qweb']._render('survey.survey_fill_form_in_progress', survey_data)

        survey_progress = False
        if answer_sudo.state == 'in_progress' and not survey_data.get('question', request.env['survey.question']).is_page:
            if survey_sudo.questions_layout == 'page_per_section':
                page_ids = survey_sudo.page_ids.ids
                survey_progress = request.env['ir.qweb']._render('survey.survey_progression', {
                    'survey': survey_sudo,
                    'page_ids': page_ids,
                    'page_number': page_ids.index(survey_data['page'].id) + (1 if survey_sudo.progression_mode == 'number' else 0)
                })
            elif survey_sudo.questions_layout == 'page_per_question':
                page_ids = (answer_sudo.predefined_question_ids.ids
                            if not answer_sudo.is_session_answer and survey_sudo.questions_selection == 'random'
                            else survey_sudo.question_ids.ids)
                survey_progress = request.env['ir.qweb']._render('survey.survey_progression', {
                    'survey': survey_sudo,
                    'page_ids': page_ids,
                    'page_number': page_ids.index(survey_data['question'].id)
                })

        background_image_url = survey_sudo.background_image_url
        if 'question' in survey_data:
            background_image_url = survey_data['question'].background_image_url
        elif 'page' in survey_data:
            background_image_url = survey_data['page'].background_image_url

        return {
            'survey_content': survey_content,
            'survey_progress': survey_progress,
            'survey_navigation': request.env['ir.qweb']._render('survey.survey_navigation', survey_data),
            'background_image_url': background_image_url
        }

