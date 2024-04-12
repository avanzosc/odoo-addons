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
    
    # Definir una nueva tabla de relación para este campo
    question_article_ids = fields.Many2many(
        'survey.question.article', 
        string='Articles',
        relation='survey_question_answer_article_rel',  # Nombre de la nueva tabla de relación
        column1='question_answer_id',  # Columna que almacena el ID de la respuesta
        column2='article_id'  # Columna que almacena el ID del artículo
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
            record.related_article_filter_ids = [(6, 0, related_articles.ids)]
            _logger.info("2024okdeb - Computed related articles for record with ID %s", record.id)
