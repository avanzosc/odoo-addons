# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _

class SurveyQuestionNormative(models.Model):
    _name = "survey.question.normative"
    _description = _("Survey Question Normative")

    name = fields.Char(
        string=_("Name"),
        required=True,
    )
    description = fields.Char(
        string=_("Description"),
    )
    error_text = fields.Text(
        string=_("Error Text"),
    )
    start_date = fields.Date(
        string=_("Start Date"),
    )
    end_date = fields.Date(
        string=_("End Date"),
    )
    related_article_ids = fields.One2many(
        "survey.question.article", 
        "question_normative_id", 
        string=_("Related Articles")
    )
