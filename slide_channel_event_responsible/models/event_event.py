# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventEvent(models.Model):
    _inherit = 'event.event'

    def write(self, values):
        confirm_stage = self.env.ref("event.event_stage_announced")
        result = super(EventEvent, self).write(values)
        if ('stage_id' in values and
                values.get('stage_id', 99) == confirm_stage.id):
            self.event_reponsibles_to_slide_channel()
        return result

    def event_reponsibles_to_slide_channel(self):
        for event in self:
            for slide_channel in event.slides_ids:
                if event.user_id:
                    slide_channel.insert_event_reponsible_in_slide_channel(
                        event, event.user_id)
                if event.main_responsible_id:
                    slide_channel.insert_event_reponsible_in_slide_channel(
                        event, event.main_responsible_id)
                if event.second_responsible_id:
                    slide_channel.insert_event_reponsible_in_slide_channel(
                        event, event.second_responsible_id)
