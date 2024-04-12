# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    notes = fields.Text(
        string="Note", help="Error Text", copy=False,
    )
    question_article_ids = fields.Many2many(
        'survey.question.article', string='Articles'
    )
    related_article_filter_ids = fields.Many2many(
        'survey.question.article',
        string="Related Articles",
        compute='_compute_related_article_filter_ids',
        store=True
    )

    @api.depends('question_id.question_normative_ids.related_article_ids')
    def _compute_related_article_filter_ids(self):
        for record in self:
            related_articles = record.question_id.question_normative_ids.mapped('related_article_ids')
            record.related_article_filter_ids = related_articles.ids
