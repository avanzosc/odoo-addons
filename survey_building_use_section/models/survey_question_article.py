# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _

class SurveyQuestionArticle(models.Model):
    _name = "survey.question.article"
    _description = _("Survey Question Article")

    name = fields.Char(
        string="Name",
        required=True,
        copy=False,
    )
    description = fields.Char(
        string="Description",
        copy=False,
    )
    error_text = fields.Text(
        string="Error Text",
        copy=False,
    )
    question_normative_id = fields.Many2one(
        "survey.question.normative",
        string="Normative", 
    )
