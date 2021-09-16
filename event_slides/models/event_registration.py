# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        for registration in self.filtered(lambda x: x.event_id.slides_ids):
            registration.create_student_in_courses()

    def create_student_in_courses(self):
        for course in self.event_id.slides_ids:
            vals = self._catch_values_for_slide_channel_partner(course)
            self.env['slide.channel.partner'].create(vals)

    def _catch_values_for_slide_channel_partner(self, course):
        vals = {'partner_id': self.student_id.id,
                'event_registration_id': self.id,
                'real_date_start': self.real_date_start,
                'real_date_end': self.real_date_end,
                'channel_id': course.id}
        return vals
