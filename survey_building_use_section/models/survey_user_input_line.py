# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)

class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    question_normative_id = fields.Many2one(
        string="Question Normative", 
        comodel_name="survey.question.normative",
    )
    notes = fields.Text(
        string="Note", 
        help="Error Text",
    )