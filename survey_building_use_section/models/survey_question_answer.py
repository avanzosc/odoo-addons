# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models, api

class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    notes = fields.Text(
        string=_("Note"),
        help=_("Error Text"),
        copy=False,
    )
    survey_id = fields.Many2one(_("survey.survey"), related="question_id.survey_id")
    matrix_survey_id = fields.Many2one(
        _("survey.survey"), related="matrix_question_id.survey_id"
    )
    question_article_ids = fields.Many2many(
        _("survey.question.article"),
        string=_("Articles"),
        relation="survey_question_answer_article_rel",
        column1="question_answer_id",
        column2="article_id",
    )
    related_article_filter_ids = fields.Many2many(
        _("survey.question.article"),
        string=_("Related Articles"),
        compute="_compute_related_article_filter_ids",
        store=True,
    )

    @api.depends(
        "matrix_question_id.question_normative_ids.related_article_ids",
        "matrix_question_id.question_normative_ids",
    )
    def _compute_related_article_filter_ids(self):
        for record in self:
            related_articles = record.matrix_question_id.question_normative_ids.mapped(
                "related_article_ids"
            )
            record.related_article_filter_ids = [(6, 0, related_articles.ids)]
