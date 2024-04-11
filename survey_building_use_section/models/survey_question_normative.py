# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class SurveyQuestionNormative(models.Model):
    _name = "survey.question.normative"
    _description = "Survey Question Normative"

    name = fields.Char(
        string="Name",
        required=True,
        copy=False,
    )
    description = fields.Char(
        string="Description",
        copy=False,
    )
    error_text = fields.Text(
        string="Error Text",
        copy=False,
    )
    start_date = fields.Date(
        string="Start Date",
        copy=False,
    )
    end_date = fields.Date(
        string="End Date",
        copy=False,
    )

