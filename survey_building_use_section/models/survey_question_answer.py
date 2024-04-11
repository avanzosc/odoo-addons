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
        'survey.question.article', string='Related Articles',
        related='question_id.question_normative_ids.normative_question_article_ids',
    )