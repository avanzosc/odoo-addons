# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    def write(self, values):
        confirm_stage = self.env.ref("event.event_stage_announced")
        cancel_stage = self.env.ref("event.event_stage_cancelled")
        done_stage = self.env.ref("event.event_stage_done")
        result = super(EventEvent, self).write(values)
        if ('stage_id' in values and
                values.get('stage_id', 99) == confirm_stage.id):
            self.update_responsibles_in_slide_channel()
        if ('stage_id' in values and
                values.get('stage_id', 99) == cancel_stage.id):
            self.update_responsibles_in_slide_channel(
                fields.Date.context_today(self))
        if ('stage_id' in values and
                values.get('stage_id', 99) == done_stage.id):
            self.update_responsibles_in_slide_channel(
                self.date_end.date())
        return result

    def update_responsibles_in_slide_channel(self, date=None):
        for event in self:
            for slide_channel in event.slides_ids:
                if event.user_id:
                    slide_channel.update_event_reponsible_in_slide_channel(
                        event, event.user_id, date)
                if event.main_responsible_id:
                    slide_channel.update_event_reponsible_in_slide_channel(
                        event, event.main_responsible_id, date)
                if event.second_responsible_id:
                    slide_channel.update_event_reponsible_in_slide_channel(
                        event, event.second_responsible_id, date)
