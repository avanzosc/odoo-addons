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
        compute="_compute_start_date",
        store=True,
        copy=False,
    )
    end_date = fields.Date(
        string="End Date",
        compute="_compute_end_date",
        store=True,
        copy=False,
    )

    @api.depends('start_year', 'end_year')
    def _compute_start_date(self):
        for record in self:
            if record.start_year and not record.start_date:
                record.start_date = fields.Date.from_string(str(record.start_year) + '-01-01')

    @api.depends('start_year', 'end_year')
    def _compute_end_date(self):
        for record in self:
            if record.end_year and not record.end_date:
                record.end_date = fields.Date.from_string(str(record.end_year) + '-12-31')
