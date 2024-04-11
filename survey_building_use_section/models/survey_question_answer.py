# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    notes = fields.Text(
        string="Note", help="Error Text", copy=False,
    )
    question_article_ids = fields.Many2many(
        'survey.question.article', string='Articles'
    )
    
    related_article_ids = fields.Many2many(
        'survey.question.article', string='Related Articles'
    )

    # Método para calcular los artículos relacionados
    def _compute_related_article_ids(self):
        for answer in self:
            if answer.question_id:  # Asegurarse de que hay una pregunta asociada
                normative_article_ids = answer.question_id.question_normative_ids.mapped('normative_question_article_ids')
                answer.related_article_ids = normative_article_ids

