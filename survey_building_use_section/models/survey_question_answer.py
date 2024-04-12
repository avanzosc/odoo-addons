# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    notes = fields.Text(
        string="Note", help="Error Text", copy=False,
    )
    question_article_ids = fields.Many2many(
        'survey.question.article', 
        string='Articles',
        relation='survey_question_answer_article_rel', 
        column1='question_answer_id', 
        column2='article_id'  
    )
    related_article_filter_ids = fields.Many2many(
        'survey.question.article',
        string="Related Articles",
        compute='_compute_related_article_filter_ids',
        store=True
    )

    @api.depends('matrix_question_id.question_normative_ids.related_article_ids')
    def _compute_related_article_filter_ids(self):
        for record in self:
            related_articles = record.matrix_question_id.question_normative_ids.mapped('related_article_ids')
            record.related_article_filter_ids = [(6, 0, related_articles.ids)]
            
            _logger.info(f"2024okdeb - {record.id} {record.related_article_filter_ids} {normative_ids} {question_ids} {related_articles}")
            _logger.info(f"2024okdeb - Se calcularon los artículos relacionados para el registro con ID {record.id} {record.value} {record} ",)
