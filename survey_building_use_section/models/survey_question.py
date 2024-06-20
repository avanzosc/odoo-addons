# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_normative_ids = fields.Many2many(
        string="Question Normatives", 
        comodel_name="survey.question.normative",
    )
    is_normative_filter = fields.Boolean(
        string="Normative Filter"
    )
    questions_to_filter = fields.Many2many(
        comodel_name="survey.question",
        relation='survey_question_filter_rel', 
        column1='questions_to_filter',  
        column2='normative_filter_question_id',
        string="Questions to filter",
    )
