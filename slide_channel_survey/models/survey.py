
from odoo import api, fields, models
import werkzeug


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    responsible_user_ids = fields.Many2one(
        'res.users', 'Input responsibles')

    header_image = fields.Binary("Header Image")

    intro_text = fields.Html('Evaluation report introduction text')

    @api.model
    def create(self, vals):
        res = super(SurveySurvey, self).create(vals)
        res._compute_responsible_users()
        return res

    def _compute_responsible_users(self):
        for res in self:
            res.responsible_user_ids = res.user_input_ids.mapped(
                'main_responsible_id') + res.user_input_ids.mapped(
                'second_responsible_id')


class SurveyUserInput(models.Model):
    _name = "survey.user_input"
    _inherit = ['survey.user_input', "mail.thread", "mail.activity.mixin", "portal.mixin"]

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

    def fix_slide_partner_relation(self):
        for record in self.filtered(lambda r: not r.slide_partner_id and not r.slide_id):
            slide_domain = [
                ('slide_type', '=', 'certification'),
                ('survey_id', '=', record.survey_id.id),]
            if record.event_id:
                slide_domain += [('channel_id', 'in', record.event_id.channel_ids.ids),]
            slide_id = self.env['slide.slide'].search(slide_domain)
            slide_partner_id = self.env['slide.slide.partner'].search([
                ('slide_id', 'in', slide_id.ids),
                ('partner_id', '=', record.partner_id.id),
            ])
            if len(slide_partner_id.ids) == 1:
                record.slide_id = slide_partner_id.slide_id.id
                record.slide_partner_id = slide_partner_id.id
