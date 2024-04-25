# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    question_normative_id = fields.Many2one(
        string=_("Question Normative"), comodel_name="survey.question.normative",
        copy=False,
    )
    notes = fields.Text(
        string=_("Note"), help=_("Error Text"), copy=False,
    )
    
    # @api.model_create_multi
    # def create(self, vals_list):
    #     lines = super(SurveyUserInputLine, self).create(vals_list)
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
    #         if (len(normatives) > 1 and
    #                 line.user_input_id.inspected_building_id.service_start_date):
    #             year = int(
    #                 line.user_input_id.inspected_building_id.service_start_date.year)
    #             for norvative in normatives:
    #                 if (norvative.start_year <= year and
    #                         norvative.end_year > year):
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
    #                     line.matrix_row_id.notes if not notes else
    #                     u"{} / {}".format(notes, line.matrix_row_id.notes)
    #                 )
    #         if notes:
    #             vals["notes"] = notes
    #         line.write(vals)




    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Filtrar vals_list para crear solo las líneas que cumplan con los criterios de tratamiento
    #     lines_filtered_vals = []
    #     for vals in vals_list:
    #         line = self.new(vals)
    #         if line.question_id and line.user_input_id.inspected_building_id.service_start_date and any(
    #             normative.start_year <= int(line.user_input_id.inspected_building_id.service_start_date.year) < normative.end_year 
    #             for normative in line.question_id.question_normative_ids
    #         ):
    #             lines_filtered_vals.append(vals)

    #     # Si hay líneas para tratar, llamar al método create del modelo padre para crearlas
    #     if lines_filtered_vals:
    #         lines_created = super(SurveyUserInputLine, self).create(lines_filtered_vals)

    #         # Filtrar las líneas creadas para el tratamiento
    #         lines_to_treat = lines_created.filtered(lambda x: any(
    #             normative.start_year <= int(x.user_input_id.inspected_building_id.service_start_date.year) < normative.end_year 
    #             for normative in x.question_id.question_normative_ids
    #         ))
    #         _logger.info("2024okdeb - Lines to treat: %s", lines_to_treat)

    #         # Si hay líneas para tratar, ejecutar _put_normative_in_line
    #         if lines_to_treat:
    #             _logger.info("2024okdeb - Processing lines_to_treat: %s", lines_to_treat)
    #             lines_to_treat._put_normative_in_line()

    #         return lines_created

    #     return self.env['survey.user_input.line']



    # def _put_normative_in_line(self):
    #     for line in self:
    #         _logger.info("2024okdeb - Processing Survey User Input Line: %s", line)

    #         normatives = line.question_id.question_normative_ids
    #         _logger.info("2024okdeb - Normatives for the question: %s", normatives)
    #         question_normative = False
    #         if len(normatives) == 1:
    #             question_normative = normatives[0]
    #             _logger.info("2024okdeb - Single normative found: %s", question_normative)
    #         if (len(normatives) > 1 and
    #                 line.user_input_id.inspected_building_id.service_start_date):
    #             year = int(
    #                 line.user_input_id.inspected_building_id.service_start_date.year)
    #             for norvative in normatives:
    #                 if (norvative.start_year <= year and
    #                         norvative.end_year > year):
    #                     question_normative = norvative
    #                     _logger.info("2024okdeb - Normative found within year range: %s", question_normative)
    #         _logger.info("2024okdeb - Question normative determined: %s", question_normative)
    #         if not question_normative:
    #             vals = {"question_normative_id": False}
    #             _logger.info("2024okdeb - No question normative found.")
    #         else:
    #             vals = {"question_normative_id": question_normative.id}
    #             _logger.info("2024okdeb - Question normative ID to be written: %s", question_normative.id)

    #         _logger.info("2024okdeb - Values to be written: %s", vals)

    #         notes = ""
    #         if not line.answer_is_correct:
    #             if question_normative and question_normative.error_text:
    #                 notes = question_normative.error_text
    #                 _logger.info("2024okdeb - Error text found for question normative: %s", notes)
    #             if line.matrix_row_id and line.matrix_row_id.notes:
    #                 notes = (
    #                     line.matrix_row_id.notes if not notes else
    #                     u"{} / {}".format(notes, line.matrix_row_id.notes)
    #                 )
    #                 _logger.info("2024okdeb - Notes found for matrix row: %s", line.matrix_row_id.notes)
    #         _logger.info("2024okdeb - Notes to be written: %s", notes)
    #         if notes:
    #             vals["notes"] = notes
    #         line.write(vals)
    #         _logger.info("2024okdeb - Line write operation complete.")

    #     _logger.info("2024okdeb - All lines processed.")