
from odoo import api, fields, models


class SlideChannelPartner(models.Model):
    _inherit = 'slide.channel.partner'

    @api.model
    def create(self, vals):
        res = super(SlideChannelPartner, self).create(vals)
        res._create_slide_channel_survey()
        return res

    def _create_slide_channel_survey(self):
        for record in self:
            slide_channel = record.channel_id
            slide_slides = slide_channel.slide_ids
            for slide in slide_slides.filtered(
                    lambda s: s.slide_type == 'certification'):
                survey_inputs = self.env['survey.user_input'].search([
                    ('survey_id', '=', slide.survey_id.id),
                    ('partner_id', '=', record.event_id.main_responsible_id.id),
                ])
                if not survey_inputs:
                    survey_input = self.env['survey.user_input'].create({
                        'survey_id': slide.survey_id.id,
                        'event_id': record.event_id.id,
                        'student_id': record.partner_id.id,
                    })
