# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    slides_ids = fields.Many2many(
        string="Courses",
        comodel_name="slide.channel",
        relation="rel_event_slides",
        column1="event_id",
        column2="slides_id",
    )

    def write(self, values):
        result = super(EventEvent, self).write(values)
        if 'slides_ids' in values:
            for event in self:
                event.recompute_courses_participants()
        return result

    def recompute_courses_participants(self):
        channel_partner_obj = self.env['slide.channel.partner']
        for registration in self.registration_ids.filtered(
                lambda x: x.state == 'open'):
            registration.create_student_in_courses()
            cond = [('partner_id', '=', registration.student_id.id),
                    ('event_registration_id', '=', registration.id),
                    ('channel_id', 'not in', self.slides_ids.ids)]
            channel_partners = channel_partner_obj.search(cond)
            if channel_partners:
                channel_partners.write(
                    {'real_date_end': fields.Date.context_today(self)})
