import logging
_logger = logging.getLogger(__name__)

from odoo import http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey

class Survey(Survey):
    @http.route()
    def survey_display_page(self, survey_token, answer_token, **post):
        res = super().survey_display_page(survey_token, answer_token, **post)
        
        # filtered_questions = []
        # for question in res.qcontext['survey'].question_and_page_ids:
        #     if question and res.qcontext['answer'].inspected_building_id.service_start_date and any(
        #         normative.start_year <= int(res.qcontext['answer'].inspected_building_id.service_start_date.year) < normative.end_year 
        #         for normative in question.question_normative_ids
        #     ):
        #         filtered_questions.append(question.id)
        
        # res.qcontext['survey'].question_and_page_ids = [(6, 0, filtered_questions)]

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
                # Verificar si alguna de las normativas cumple con la condición
                for normative in all_normatives:
                    if (normative.start_year <= res.qcontext['answer'].inspected_building_id.service_start_date.year < normative.end_year
                        and not answer in selected_answers 
                        and answer.value in normative.name):
                        # Crear un registro para survey.user_input_line
                        user_input_line = request.env['survey.user_input.line'].create({
                            'survey_id': res.qcontext['survey'].id,
                            'question_id': triggering_question_obj.id,
                            'answer_type': 'suggestion',
                            'suggested_answer_id': answer.id,
                            'user_input_id': res.qcontext['answer'].id
                        })
                        
                        selected_answers.append(answer)                        

        return request.render('survey.survey_page_fill',
            self._prepare_survey_data(res.qcontext['survey'], res.qcontext['answer'], **post))
