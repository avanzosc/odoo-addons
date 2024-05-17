# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def action_send_survey(self):
        result = super().action_send_survey()
        result["name"] = _("Create Survey to Building")
        return result

    def add_normative_filter(self):
        question_obj = self.env["survey.question"]
        answer_obj = self.env["survey.question.answer"]
        normative_obj = self.env["survey.question.normative"]
        for survey in self:
            existing_normative_filter = survey.question_and_page_ids.filtered(
                lambda q: q.is_normative_filter
            )
            normative_filter_existed = False
            if existing_normative_filter:
                existing_normative_filter.unlink()
                normative_filter_existed = True

            normative_filter_question = question_obj.create(
                {
                    "survey_id": survey.id,
                    "title": _("NORMATIVE FILTER"),
                    "question_type": "multiple_choice",
                    "description": _(
                        "Question needed to trigger normative questions and "
                        "filter questions by normative"
                    ),
                    "is_normative_filter": True,
                    "sequence": 1,
                }
            )

            if not normative_filter_existed:
                for question_page in survey.question_and_page_ids:
                    question_page.sequence += 10

            existing_answers = normative_filter_question.suggested_answer_ids
            existing_answers.unlink()

            normative_data = normative_obj.search([])

            for normative in normative_data:
                answer_obj.create(
                    {
                        "question_id": normative_filter_question.id,
                        "value": normative.name,
                        "sequence": normative.id,
                        "notes": normative.description,
                    }
                )
