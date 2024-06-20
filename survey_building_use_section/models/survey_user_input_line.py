# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    question_normative_id = fields.Many2one(
        "survey.question.normative",
        "Question Normative",
    )
    notes = fields.Text(
        "Note",
        help="Error Text",
    )
