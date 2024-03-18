from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'
    _description = 'Survey Question'

    image = fields.Image(
        string='Question Image'
    )