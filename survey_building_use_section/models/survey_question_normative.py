# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


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
    normative_question_article_ids = fields.One2many(
        "survey.question.article",
        inverse_name="question_normative_id",
        string="Question Articles",
    )
    start_year = fields.Integer(
        string="Start Year",
        copy=False,
    )
    end_year = fields.Integer(
        string="End Year",
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
    
    def write(self, values):
        if 'start_year' in values:
            start_year = values['start_year']
            start_date = fields.Date.from_string(str(start_year) + '-01-01')
            values['start_date'] = start_date
        if 'end_year' in values:
            end_year = values['end_year']
            end_date = fields.Date.from_string(str(end_year) + '-12-31')
            values['end_date'] = end_date
        return super().write(values)

    def create(self, values):
        if 'start_year' in values:
            start_year = values['start_year']
            start_date = fields.Date.from_string(str(start_year) + '-01-01')
            values['start_date'] = start_date
        if 'end_year' in values:
            end_year = values['end_year']
            end_date = fields.Date.from_string(str(end_year) + '-12-31')
            values['end_date'] = end_date
        return super().create(values)
