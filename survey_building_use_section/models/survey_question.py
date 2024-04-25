# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _

class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_normative_ids = fields.Many2many(
        string=_("Question Normatives"), comodel_name="survey.question.normative",
    )
    is_normative_filter = fields.Boolean(string=_("Normative Filter"))
