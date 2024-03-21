# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    question_normative_id = fields.Many2one(
        string="Question Normative", comodel_name="survey.question.normative",
        copy=False,
    )
    notes = fields.Text(
        string="Note", help="Error Text", copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info("2024okdeb - Creating Survey User Input Lines with values: %s", vals_list)

        lines = super(SurveyUserInputLine, self).create(vals_list)
        _logger.info("2024okdeb - Creating Survey User Input Lines with lines: %s", lines)

        lines_to_treat = lines.filtered(
            lambda x: x.question_id and 
            x.user_input_id.inspected_building_id.service_start_date and 
            any(normative.start_year <= int(x.user_input_id.inspected_building_id.service_start_date.year) < normative.end_year 
            for normative in x.question_id.question_normative_ids)
        )

        _logger.info("2024okdeb - Creating Survey User Input Lines with lines_to_treat: %s", lines_to_treat)


        if lines_to_treat:
            _logger.info("2024okdeb - Processing lines_to_treat: %s", lines_to_treat)

            lines_to_treat._put_normative_in_line()
        return lines_to_treat

    def _put_normative_in_line(self):
        for line in self:
            _logger.info("2024okdeb - Processing Survey User Input Line: %s", line)

            normatives = line.question_id.question_normative_ids
            _logger.info("2024okdeb - Normatives for the question: %s", normatives)
            question_normative = False
            if len(normatives) == 1:
                question_normative = normatives[0]
                _logger.info("2024okdeb - Single normative found: %s", question_normative)
            if (len(normatives) > 1 and
                    line.user_input_id.inspected_building_id.service_start_date):
                year = int(
                    line.user_input_id.inspected_building_id.service_start_date.year)
                for norvative in normatives:
                    if (norvative.start_year <= year and
                            norvative.end_year > year):
                        question_normative = norvative
                        _logger.info("2024okdeb - Normative found within year range: %s", question_normative)
            _logger.info("2024okdeb - Question normative determined: %s", question_normative)
            if not question_normative:
                vals = {"question_normative_id": False}
                _logger.info("2024okdeb - No question normative found.")
            else:
                vals = {"question_normative_id": question_normative.id}
                _logger.info("2024okdeb - Question normative ID to be written: %s", question_normative.id)

            _logger.info("2024okdeb - Values to be written: %s", vals)

            notes = ""
            if not line.answer_is_correct:
                if question_normative and question_normative.error_text:
                    notes = question_normative.error_text
                    _logger.info("2024okdeb - Error text found for question normative: %s", notes)
                if line.matrix_row_id and line.matrix_row_id.notes:
                    notes = (
                        line.matrix_row_id.notes if not notes else
                        u"{} / {}".format(notes, line.matrix_row_id.notes)
                    )
                    _logger.info("2024okdeb - Notes found for matrix row: %s", line.matrix_row_id.notes)
            _logger.info("2024okdeb - Notes to be written: %s", notes)
            if notes:
                vals["notes"] = notes
            line.write(vals)
            _logger.info("2024okdeb - Line write operation complete.")

        _logger.info("2024okdeb - All lines processed.")



    # @api.model_create_multi
    # def create(self, vals_list):
    #     lines = self._filter_questions_of_normative(vals_list)
    #     lines_to_treat = lines.filtered(lambda x: x.question_id)
    #     if lines_to_treat:
    #         lines_to_treat._put_normative_in_line()
    #     return lines

    # def _put_normative_in_line(self):
    #     for line in self:
    #         normatives = line.question_id.question_normative_ids
    #         question_normative = False
    #         if len(normatives) == 1:
    #             question_normative = normatives[0]
    #         if (
    #             len(normatives) > 1
    #             and line.user_input_id.inspected_building_id.service_start_date
    #         ):
    #             year = int(
    #                 line.user_input_id.inspected_building_id.service_start_date.year
    #             )
    #             for norvative in normatives:
    #                 if norvative.start_year <= year and norvative.end_year > year:
    #                     question_normative = norvative
    #         if not question_normative:
    #             vals = {"question_normative_id": False}
    #         else:
    #             vals = {"question_normative_id": question_normative.id}
    #         notes = ""
    #         if not line.answer_is_correct:
    #             if question_normative and question_normative.error_text:
    #                 notes = question_normative.error_text
    #             if line.matrix_row_id and line.matrix_row_id.notes:
    #                 notes = (
    #                     line.matrix_row_id.notes
    #                     if not notes
    #                     else "{} / {}".format(notes, line.matrix_row_id.notes)
    #                 )
    #         if notes:
    #             vals["notes"] = notes
    #         line.write(vals)

    # def _filter_questions_of_normative(self, vals):
    #     if "question_normative_id" in vals:
    #         question_normative_id = vals.get("question_normative_id")
    #         if not self._is_normative_valid(question_normative_id):
    #             raise ValidationError(
    #                 "La normativa seleccionada no es válida para el edificio inspeccionado."
    #             )
    #     return super(SurveyUserInputLine, self).create(vals)

    # def _is_normative_valid(self, question_normative_id):
    #     user_input = self.env.context.get("user_input_id", False)
    #     if user_input:
    #         inspected_building = (
    #             self.env["survey.user_input"].browse(user_input).inspected_building_id
    #         )
    #         return question_normative_id in inspected_building.normativas_ids.ids
    #     return False