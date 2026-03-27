# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    calculated_matrix_question_ids = fields.Many2many(
        comodel_name="survey.question.answer",
        relation="survey_user_input_line_matrix_answer_rel",
        column1="user_input_line_id",
        column2="question_answer_id",
        string="Matrix Question Answers",
        compute="_compute_matrix_question_id",
        store=True,
    )

    calculated_suggested_answer_question_ids = fields.Many2many(
        comodel_name="survey.question.answer",
        relation="survey_user_input_line_suggested_answer_rel",
        column1="user_input_line_id",
        column2="question_answer_id",
        string="Suggested Answer Questions",
        compute="_compute_suggested_answer_id",
        store=True,
    )

    @api.depends("matrix_row_id", "matrix_row_id.matrix_question_id")
    def _compute_matrix_question_id(self):
        for line in self:
            if line.matrix_row_id and line.matrix_row_id.matrix_question_id:
                line.calculated_matrix_question_ids = (
                    line.matrix_row_id.matrix_question_id.matrix_row_ids
                )
            else:
                line.calculated_matrix_question_ids = False

    @api.depends("suggested_answer_id", "suggested_answer_id.question_id")
    def _compute_suggested_answer_id(self):
        for line in self:
            if line.suggested_answer_id and line.suggested_answer_id.question_id:
                line.calculated_suggested_answer_question_ids = (
                    line.suggested_answer_id.question_id.suggested_answer_ids
                )
            else:
                line.calculated_suggested_answer_question_ids = False
