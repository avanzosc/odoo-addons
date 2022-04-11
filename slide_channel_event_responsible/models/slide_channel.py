# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models,fields


class SlideQuestion(models.Model):
    _inherit = 'slide.question'
    answer_ids = fields.One2many(copy=True)


class SlideSlide(models.Model):
    _inherit = 'slide.slide'
    question_ids = fields.One2many(copy=True)


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    def update_event_reponsible_in_slide_channel(self, event, responsible,
                                                 date):
        slide_channel_partner_obj = self.env['slide.channel.partner']
        cond = [('channel_id', '=', self.id),
                ('partner_id', '=', responsible.partner_id.id)]
        slide_channel = slide_channel_partner_obj.search(cond, limit=1)
        if not date:
            if not slide_channel:
                self.create_responsible_in_slide_channel(
                    event, responsible.partner_id)
            else:
                if slide_channel.real_date_end:
                    slide_channel.write({
                        'real_date_start': event.date_begin.date(),
                        'real_date_end': False})
        if date and slide_channel:
            events = self.event_ids.filtered(
                lambda x: x.id != event.id and not x.stage_id.pipe_end and
                (x.user_id and x.user_id == responsible) or
                (x.main_responsible_id and
                 x.main_responsible_id == responsible) or
                (x.second_responsible_id == responsible))
            if (not events or
                    (events and len(events) == 1) and event == event):
                slide_channel.write({'real_date_end': date})

    def create_responsible_in_slide_channel(self, event, partner):
        slide_channel_partner_obj = self.env['slide.channel.partner']
        vals = {
            'channel_id': self.id,
            'partner_id': partner.id,
            'partner_email': partner.email,
            'real_date_start': event.date_begin.date(),
            'real_date_end': False
            }
        slide_channel_partner_obj.create(vals)
