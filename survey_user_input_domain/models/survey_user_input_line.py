# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    calculated_matrix_question_id = fields.Many2one(
        comodel_name="survey.question",
        string="Matrix Question ID",
        compute="_compute_matrix_question_id",
        store=True,
    )
    calculated_suggested_answer_question_id = fields.Many2one(
        comodel_name="survey.question",
        string="Suggested Answer ID",
        compute="_compute_suggested_answer_id",
        store=True,
    )

    @api.depends("matrix_row_id", "matrix_row_id.matrix_question_id")
    def _compute_matrix_question_id(self):
        for line in self:
            line.calculated_matrix_question_id = (
                line.matrix_row_id.matrix_question_id if line.matrix_row_id else False
            )

    @api.depends("suggested_answer_id", "suggested_answer_id.question_id")
    def _compute_suggested_answer_id(self):
        for line in self:
            line.calculated_suggested_answer_question_id = (
                line.suggested_answer_id.question_id
                if line.suggested_answer_id
                else False
            )
