# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _

class SurveyQuestionNormative(models.Model):
    _name = "survey.question.normative"
    _description = _("Survey Question Normative")

    name = fields.Char(
        string="Name",
        required=True,
    )
    description = fields.Char(
        string="Description",
    )
    error_text = fields.Text(
        string="Error Text",
    )
    start_date = fields.Date(
        string="Start Date",
        required=True,
    )
    end_date = fields.Date(
        string="End Date",
        required=True,
    )
    related_article_ids = fields.One2many(
        "survey.question.article", 
        "question_normative_id", 
        string="Related Articles"
    )
