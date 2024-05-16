# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SurveyQuestionNormative(models.Model):
    _name = "survey.question.normative"
    _description = "Survey Question Normative"

    name = fields.Char(
        required=True,
        copy=False,
    )
    description = fields.Char(
        copy=False,
    )
    error_text = fields.Text(
        copy=False,
    )
    start_date = fields.Date(
        copy=False,
    )
    end_date = fields.Date(
        copy=False,
    )
    related_article_ids = fields.One2many(
        comodel_name="survey.question.article",
        inverse_name="question_normative_id",
        string="Related Articles",
    )
