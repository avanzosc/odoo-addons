# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SurveyQuestionArticle(models.Model):
    _name = "survey.question.article"
    _description = "Survey Question Article"

    name = fields.Char(
        "Name",
        required=True,
        copy=False,
    )
    description = fields.Char(
        "Description",
        copy=False,
    )
    error_text = fields.Text(
        "Error Text",
        copy=False,
    )
    question_normative_id = fields.Many2one(
        "survey.question.normative",
        "Normative",
    )
