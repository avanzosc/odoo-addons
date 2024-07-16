from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"
    _description = "Survey Question"

    image = fields.Image(string="Question Image")
