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
            #     triggering_question_id = normative_filter_question.id

            # else:
            #     triggering_question_id = existing_normative_filter.id


