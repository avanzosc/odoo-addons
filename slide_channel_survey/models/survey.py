
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    responsible_user_ids = fields.Many2one(
        'res.users', 'Input responsibles')

    def create(self, vals):
        res = self.super().create(self, vals)
        res._compute_responsible_users()
        return res

    def _compute_responsible_users(self):
        for res in self:
            res.responsible_user_ids = res.user_input_ids.mapped(
                'main_responsible_id') + res.user_input_ids.mapped(
                'second_responsible_id')


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    student_id = fields.Many2one('res.partner', 'Student')
    event_id = fields.Many2one('event.event', 'Event')
    main_responsible_id = fields.Many2one(
        'res.users', 'Main responsible',
        related='event_id.main_responsible_id')
    second_responsible_id = fields.Many2one(
        'res.users', 'Second responsible',
        related='event_id.second_responsible_id')
