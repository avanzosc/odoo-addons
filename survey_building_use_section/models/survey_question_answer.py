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
            _logger.info("2024okdeb - Comenzando a calcular artículos relacionados para el registro con ID %s", record.id)
            question_ids = record.question_id
            _logger.info("2024okdeb - Se obtuvieron los IDs de pregunta para el registro con ID %s", record.id)
            
            normative_ids = question_ids.question_normative_ids
            _logger.info("2024okdeb - Se obtuvieron los IDs normativos para el registro con ID %s", record.id)
            
            related_articles = normative_ids.mapped('related_article_ids')
            _logger.info("2024okdeb - Se mapearon los IDs de artículos relacionados para el registro con ID %s", record.id)
            
            record.related_article_filter_ids = [(6, 0, related_articles.ids)]
            _logger.info("2024okdeb - Se asignaron los IDs de artículos relacionados para el registro con ID %s", record.id)
            
            _logger.info("2024okdeb - Se calcularon los artículos relacionados para el registro con ID %s", record.id)
