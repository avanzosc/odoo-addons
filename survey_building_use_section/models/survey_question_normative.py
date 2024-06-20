# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SurveyQuestionNormative(models.Model):
    _name = "survey.question.normative"
    _description = "Survey Question Normative"

    name = fields.Char(
        "Name",
        required=True,
    )
    description = fields.Char(
        "Description",
    )
    error_text = fields.Text(
        "Error Text",
    )
    start_date = fields.Date(
        "Start Date",
        required=True,
    )
    end_date = fields.Date(
        "End Date",
        required=True,
    )
    related_article_ids = fields.One2many(
        "survey.question.article", "question_normative_id", "Related Articles"
    )
