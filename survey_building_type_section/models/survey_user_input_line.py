# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    question_normative_id = fields.Many2one(
        string="Question Normative",
        comodel_name="survey.question.normative",
        copy=False,
    )
    notes = fields.Text(
        string="Note",
        help="Error Text",
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines_to_treat = lines.filtered(lambda x: x.question_id)
        if lines_to_treat:
            lines_to_treat._put_normative_in_line()
        return lines

    def _put_normative_in_line(self):
        for line in self:
            normatives = line.question_id.question_normative_ids
            question_normative = False
            if len(normatives) == 1:
                question_normative = normatives[0]
            if (
                len(normatives) > 1
                and line.user_input_id.inspected_building_id.service_start_date
            ):
                year = int(
                    line.user_input_id.inspected_building_id.service_start_date.year
                )
                for norvative in normatives:
                    if norvative.start_year <= year and norvative.end_year > year:
                        question_normative = norvative
            if not question_normative:
                vals = {"question_normative_id": False}
            else:
                vals = {"question_normative_id": question_normative.id}
            notes = ""
            if not line.answer_is_correct:
                if question_normative and question_normative.error_text:
                    notes = question_normative.error_text
                if line.matrix_row_id and line.matrix_row_id.notes:
                    notes = (
                        line.matrix_row_id.notes
                        if not notes
                        else "{} / {}".format(notes, line.matrix_row_id.notes)
                    )
            if notes:
                vals["notes"] = notes
            line.write(vals)
