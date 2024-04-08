import pprint
import logging

_logger = logging.getLogger(__name__)

from odoo import http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey
from odoo.addons.survey.controllers.survey_session_manage import UserInputSession


class Survey(Survey):
    @http.route()
    def survey_display_page(self, survey_token, answer_token, **post):
        res = super().survey_display_page(survey_token, answer_token, **post)
        
        triggering_question_id = request.env['survey.question'].search([('survey_id', '=', res.qcontext['survey'].id), ('is_normative_filter', '=', True)], limit=1).id
        
        if triggering_question_id:
            triggering_question_obj = request.env['survey.question'].browse(triggering_question_id)

            for question in res.qcontext['survey'].question_and_page_ids:
                if question.sequence > triggering_question_obj.sequence:
                    triggered_question = question                
                    # All the questions must be conditional. If they are not conditional they will display 
                    # no matter the condition
                    triggered_question.write({
                        'is_conditional': True,
                        'triggering_question_id': triggering_question_id,
                        'triggering_answer_id': False,
                    })

                    if any(normative.start_year <= res.qcontext['answer'].inspected_building_id.service_start_date.year < normative.end_year
                        for normative in question.question_normative_ids):
                        matched_normatives = [normative for normative in question.question_normative_ids if normative.start_year <= res.qcontext['answer'].inspected_building_id.service_start_date.year < normative.end_year]
                        matching_normative_names = [normative.name for normative in matched_normatives]
                        matched_answers = [ans for ans in triggering_question_obj.suggested_answer_ids if ans.value in matching_normative_names]
                        if matched_answers:
                            triggering_answer = next((ans for ans in triggering_question_obj.suggested_answer_ids if ans.value == matched_answers[0].value), False)
                            if triggering_answer:
                                triggered_question.write({
                                    'triggering_answer_id': triggering_answer.id,
                                })
                                
                # Write a value in triggering_answer_id not to be null
                # Get the first normative of the question. This answer will not trigger the question 
                # so id does not matter if it is the first or the last
                triggering_answer = next((ans for ans in triggering_question_obj.suggested_answer_ids if ans.value in [normative.name for normative in question.question_normative_ids]), False)
                if not question.triggering_answer_id and triggering_answer:
                    question.write({
                        'triggering_answer_id': triggering_answer.id,
                    })


            # Seleccionar las respuestas basadas en la lógica dada
            selected_answers = []

            # Obtener todas las normativas de la tabla survey.question.normative
            all_normatives = request.env['survey.question.normative'].search([])

            for answer in triggering_question_obj.suggested_answer_ids:                
                for normative in all_normatives:
                    # Verificar si alguna de las normativas cumple con la condición
                    if (normative.start_year <= res.qcontext['answer'].inspected_building_id.service_start_date.year < normative.end_year
                        and answer not in selected_answers 
                        and answer.value == normative.name):
                        
                        _logger.info(f"2024okdeb - Condition evaluated: {normative.start_year} <= {res.qcontext['answer'].inspected_building_id.service_start_date.year} < {normative.end_year} - Normative name: {normative.name} - Answer value: {answer.value}")

                        
                        # Verificar si ya existe un registro para estas condiciones
                        existing_user_input_line = request.env['survey.user_input.line'].search([
                            ('survey_id', '=', res.qcontext['survey'].id),
                            ('question_id', '=', triggering_question_obj.id),
                            ('answer_type', '=', 'suggestion'),
                            ('suggested_answer_id', '=', answer.id),
                            ('user_input_id', '=', res.qcontext['answer'].id)
                        ])

                        if not existing_user_input_line:
                            # Logging the condition evaluation

                            # Create a record for survey.user_input_line
                            user_input_line = request.env['survey.user_input.line'].create({
                                'survey_id': res.qcontext['survey'].id,
                                'question_id': triggering_question_obj.id,
                                'answer_type': 'suggestion',
                                'suggested_answer_id': answer.id,
                                'user_input_id': res.qcontext['answer'].id
                            })
                        
                            _logger.info(f"2024okdeb - Created survey.user_input.line with id {user_input_line.id}")

                        else:
                            _logger.info(f"2024okdeb - Survey exists: {existing_user_input_line}")

                        
                        selected_answers.append(answer)                        

        return request.render('survey.survey_page_fill',
            self._prepare_survey_data(res.qcontext['survey'], res.qcontext['answer'], **post))

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        res = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        pprint_string = pprint.pformat(res, indent=4)
        _logger.info(f"\n\n2024okdeb - Contenido de res pprint:\n{pprint_string}")
        _logger.info(f"\n\n2024okdeb - Contenido de res:\n{res}")
        return res

    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        _logger.info(f"\n\n2024okdeb - Contenido de res2 survey_sudo:\n{survey_sudo}")
        _logger.info(f"\n\n2024okdeb - Contenido de res2 answer_sudo:\n{answer_sudo}")
        res = super()._prepare_question_html(survey_sudo, answer_sudo, **post)
        _logger.info(f"\n\n2024okdeb - Contenido de res2:\n{res}")
        return res

    def survey_submit(self, survey_token, answer_token, **post):
        """ Submit a page from the survey.
        This will take into account the validation errors and store the answers to the questions.
        If the time limit is reached, errors will be skipped, answers will be ignored and
        survey state will be forced to 'done'"""
        # Survey Validation
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
        if access_data['validity_code'] is not True:
            return {'error': access_data['validity_code']}
        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']

        if answer_sudo.state == 'done':
            return {'error': 'unauthorized'}

        questions, page_or_question_id = survey_sudo._get_survey_questions(answer=answer_sudo,
                                                                           page_id=post.get('page_id'),
                                                                           question_id=post.get('question_id'))

        if not answer_sudo.test_entry and not survey_sudo._has_attempts_left(answer_sudo.partner_id, answer_sudo.email, answer_sudo.invite_token):
            # prevent cheating with users creating multiple 'user_input' before their last attempt
            return {'error': 'unauthorized'}

        if answer_sudo.survey_time_limit_reached or answer_sudo.question_time_limit_reached:
            if answer_sudo.question_time_limit_reached:
                time_limit = survey_sudo.session_question_start_time + relativedelta(
                    seconds=survey_sudo.session_question_id.time_limit
                )
                time_limit += timedelta(seconds=3)
            else:
                time_limit = answer_sudo.start_datetime + timedelta(minutes=survey_sudo.time_limit)
                time_limit += timedelta(seconds=10)
            if fields.Datetime.now() > time_limit:
                # prevent cheating with users blocking the JS timer and taking all their time to answer
                return {'error': 'unauthorized'}

        errors = {}
        # Prepare answers / comment by question, validate and save answers
        for question in questions:
            inactive_questions = request.env['survey.question'] if answer_sudo.is_session_answer else answer_sudo._get_inactive_conditional_questions()
            if question in inactive_questions:  # if question is inactive, skip validation and save
                continue
            answer, comment = self._extract_comment_from_answers(question, post.get(str(question.id)))
            errors.update(question.validate_question(answer, comment))
            if not errors.get(question.id):
                answer_sudo.save_lines(question, answer, comment)

        if errors and not (answer_sudo.survey_time_limit_reached or answer_sudo.question_time_limit_reached):
            return {'error': 'validation', 'fields': errors}

        if not answer_sudo.is_session_answer:
            answer_sudo._clear_inactive_conditional_answers()

        if answer_sudo.survey_time_limit_reached or survey_sudo.questions_layout == 'one_page':
            answer_sudo._mark_done()
        elif 'previous_page_id' in post:
            # when going back, save the last displayed to reload the survey where the user left it.
            answer_sudo.write({'last_displayed_page_id': post['previous_page_id']})
            # Go back to specific page using the breadcrumb. Lines are saved and survey continues
            return self._prepare_question_html(survey_sudo, answer_sudo, **post)
        else:
            if not answer_sudo.is_session_answer:
                next_page = survey_sudo._get_next_page_or_question(answer_sudo, page_or_question_id)
                if not next_page:
                    answer_sudo._mark_done()

            answer_sudo.write({'last_displayed_page_id': page_or_question_id})

        _logger.info(f"\n\n2024okdeb - Contenido de res2 survey_sudo:\n{survey_sudo}")
        _logger.info(f"\n\n2024okdeb - Contenido de res2 answer_sudo:\n{answer_sudo}")


        return self._prepare_question_html(survey_sudo, answer_sudo)



# class UserInputSession(UserInputSession):
#     @http.route()
#     def survey_session_next_question(self, survey_token, go_back=False, **kwargs):
#         res = super.survey_session_next_question(survey_token, go_back, **kwargs)
#         pprint_string = pprint.pformat(res, indent=4)
#         _logger.info(f"\n\n2024okdeb - Contenido de res3 pprint:\n{pprint_string}")
#         _logger.info(f"\n\n2024okdeb - Contenido de res3:\n{res}")
#         return res
