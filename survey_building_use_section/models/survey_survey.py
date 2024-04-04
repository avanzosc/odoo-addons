# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def action_send_survey(self):
        result = super(SurveySurvey, self).action_send_survey()
        result["name"] = _("Create Survey to Building")
        return result

    def add_normative_filter(self):
        for survey in self:
            existing_normative_filter = survey.question_and_page_ids.filtered(lambda q: q.is_normative_filter)
            if not existing_normative_filter:
                normative_filter_question = self.env['survey.question'].create({
                    'survey_id': survey.id,
                    'title': 'NORMATIVE FILTER',
                    'description': 'Question needed to trigger normative questions and filter questions by normative',
                    'is_normative_filter': True,
                    'sequence': 1
                })
                existing_answers = normative_filter_question.suggested_answer_ids
                existing_answers.unlink()

                normative_data = self.env['survey.question.normative'].search([])
                for normative in normative_data:
                    possible_answer = self.env['survey.question.answer'].create({
                        'question_id': normative_filter_question.id,
                        'value': normative.name,
                        'sequence': normative.id,
                        'notes': normative.description
                    })
                triggering_question_id = normative_filter_question.id

            else:
                triggering_question_id = existing_normative_filter.id

            for question in survey.question_and_page_ids:
                if question.sequence > triggering_question_id:
                    triggering_question = question
                    for answer in triggering_question.suggested_answer_ids:
                        if any(normative.start_year <= answer.inspected_building_id.service_start_date.year < normative.end_year
                            for normative in answer.question_id.question_normative_ids):
                            matched_normatives = [normative for normative in answer.question_id.question_normative_ids if normative.start_year <= answer.inspected_building_id.service_start_date.year < normative.end_year]
                            matching_normative_names = [normative.name for normative in matched_normatives]
                            triggering_question_obj = self.env['survey.question'].browse(triggering_question_id)
                            matched_answers = [ans for ans in triggering_question_obj.suggested_answer_ids if ans.value.get('en_US') in matching_normative_names]
                            if matched_answers:
                                triggering_answer = next((ans for ans in triggering_question_obj.suggested_answer_ids if ans.value.get('en_US') == matched_answers[0].value.get('en_US')), False)
                                if triggering_answer:
                                    triggering_question.write({'triggering_question_id': triggering_question_id,
                                                            'triggering_answer_id': triggering_answer.id})
                                    break
