
from odoo import fields, models
import werkzeug


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    responsible_user_ids = fields.Many2one(
        'res.users', 'Input responsibles')

    def create(self, vals):
        res = super(SurveySurvey, self).create(self, vals)
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

    def button_open_website_surveys(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        url = werkzeug.urls.url_join(base_url, self.get_start_url())
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

