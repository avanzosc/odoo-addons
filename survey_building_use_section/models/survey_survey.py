# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, models

from odoo.addons.survey_building_use_section.controllers.main import Survey

_logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def action_send_survey(self):
        result = super().action_send_survey()
        result["name"] = _("Create Survey to Building")
        return result

    def add_normative_filter(self):
        for survey in self:
            existing_normative_filter = survey.question_and_page_ids.filtered(
                lambda q: q.is_normative_filter
            )
            normative_filter_existed = False
            if existing_normative_filter:
                # existing_normative_filter.unlink()
                normative_filter_existed = True

            normative_filter_question = self.env["survey.question"].create(
                {
                    "survey_id": survey.id,
                    "title": _("NORMATIVE FILTER"),
                    "question_type": "multiple_choice",
                    "description": _(
                        "Question needed to trigger normative questions and filter questions by normative"
                    ),
                    "is_normative_filter": True,
                    "sequence": 1,
                }
            )

            if not normative_filter_existed:
                for question_page in survey.question_and_page_ids:
                    question_page.sequence += 10

            # existing_answers = normative_filter_question.suggested_answer_ids
            # existing_answers.unlink()

            normative_data = self.env["survey.question.normative"].search([])
            for normative in normative_data:
                self.env["survey.question.answer"].create(
                    {
                        "question_id": normative_filter_question.id,
                        "value": normative.name,
                        "sequence": normative.id,
                        "notes": normative.description,
                    }
                )

            # Remove all the normative filter triggering_questions to do the filter again correctly
            questions = self.env["survey.question"].search(
                [("survey_id", "=", survey.id)]
            )

            for question in questions:
                if question.triggering_question_id.is_normative_filter:
                    question.write(
                        {
                            "is_conditional": False,
                            "triggering_question_id": False,
                            "triggering_answer_id": False,
                        }
                    )

    def _create_and_fill_normative_filters(
        self, current_survey_id, current_user_input_id
    ):
        triggering_question_ids = self.env["survey.question"].search(
            [
                ("survey_id", "=", current_survey_id.id),
                ("is_normative_filter", "=", True),
            ]
        )

        Survey._create_and_fill_normative_filters_logic(
            current_survey_id, current_user_input_id, triggering_question_ids
        )
