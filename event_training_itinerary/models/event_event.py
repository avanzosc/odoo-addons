# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    training_itinerary_id = fields.Many2one(
        string='Training itinerary', comodel_name='slide.channel.tag')
    training_itinerary_courses_count = fields.Integer(
        string='Itinerary courses number', store=True,
        related='training_itinerary_id.courses_count')
    event_courses_count = fields.Integer(
        string='Courses number')
    different_course_counters = fields.Boolean(
        string='Different course counters', store=True,
        compute='_compute_different_course_counters')

    @api.depends('training_itinerary_courses_count', 'event_courses_count')
    def _compute_different_course_counters(self):
        for event in self:
            if (event.training_itinerary_courses_count ==
                    event.event_courses_count):
                event.different_course_counters = False
            else:
                event.different_course_counters = True

    def delete_courses_not_in_itinerary(self):
        for event in self.filtered(lambda x: x.training_itinerary_id):
            slides = event.slides_ids.filtered(
                lambda z: event.training_itinerary_id not in z.tag_ids)
            for slide in slides:
                event.slides_ids = [(3, slide.id)]

    def bring_courses_with_itinerary(self):
        for event in self.filtered(lambda x: x.training_itinerary_id):
            cond = [('tag_ids', 'in', event.training_itinerary_id.ids)]
            courses = self.env['slide.channel'].search(cond)
            for course in courses:
                if course not in event.slides_ids:
                    event.slides_ids = [(4, course.id)]

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        if event.slides_ids:
            event.calculate_event_courses_count()
        return event

    def write(self, vals):
        res = super(EventEvent, self).write(vals)
        if 'slides_ids' in vals:
            self.calculate_event_courses_count()
        return res

    def ir_cron_calculate_courses_count(self):
        cond = []
        events = self.env['event.event'].search(cond)
        events.calculate_event_courses_count()

    def calculate_event_courses_count(self):
        for event in self:
            event.event_courses_count = len(event.slides_ids)
