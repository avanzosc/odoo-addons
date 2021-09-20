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

    def write(self, vals):
        result = super(EventRegistration, self).write(vals)
        if (('real_date_start' in vals and
             vals.get('real_date_start', False)) or
             ('real_date_end' in vals and
                vals.get('real_date_end', False))):
            self.update_course_participant_real_dates(vals)
        return result


    def update_course_participant_real_dates(self, vals):
        channel_partner_obj = self.env['slide.channel.partner']
        for registration in self.filtered(lambda x: x.event_id.slides_ids):
            for course in registration.event_id.slides_ids:
                cond = [('partner_id', '=', registration.student_id.id),
                        ('event_registration_id', '=', registration.id),
                        ('channel_id', '=', course.id)]
                channel_partner = channel_partner_obj.search(cond)
                if channel_partner:
                    vals2 = {}
                    if ('real_date_start' in vals and
                            vals.get('real_date_start', False)):
                        vals2['real_date_start'] = vals.get('real_date_start')
                    if ('real_date_end' in vals and
                            vals.get('real_date_end', False)):
                        vals2['real_date_end'] = vals.get('real_date_end')
                    channel_partner.write(vals2)
