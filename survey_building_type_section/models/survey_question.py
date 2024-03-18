# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_normative_ids = fields.Many2many(
        string="Question Normatives",
        comodel_name="survey.question.normative",
        copy=False,
    )
