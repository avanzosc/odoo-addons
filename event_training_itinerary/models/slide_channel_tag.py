# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _


class SlideChannelTag(models.Model):
    _inherit = 'slide.channel.tag'

    tag_course_ids = fields.One2many(
        string='Courses of Training itinerary',
        comodel_name='slide.channel.tag.course',
        inverse_name='slide_channel_tag_id')
    courses_count = fields.Integer(
        string='Courses number', compute='_compute_courses_count',
        store=True)

    @api.depends("tag_course_ids")
    def _compute_courses_count(self):
        for tag in self:
            tag.courses_count = len(tag.tag_course_ids)

    def action_view_courses(self):
        if not self.tag_course_ids:
            return
        return {
            'name': _("Training itinerary courses"),
            'view_mode': 'tree',
            'res_model': 'slide.channel.tag.course',
            'domain': [('id', 'in', self.tag_course_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': self.env.context.copy()
        }

    def bring_courses(self):
        for tag in self:
            cond = [('tag_ids', 'in', tag.ids)]
            courses = self.env['slide.channel'].search(cond)
            for course in tag.tag_course_ids:
                if course.slide_channel_id not in courses:
                    course.unlink()
            for course in courses:
                if not tag.tag_course_ids:
                    line = False
                else:
                    line = tag.tag_course_ids.filtered(
                        lambda x: x.slide_channel_id == course)
                if not line:
                    vals = {'slide_channel_id': course.id}
                    tag.tag_course_ids = [(0, 0, vals)]

    def action_duplicate(self):
        default = {'name': u'{} {}'.format(self.name, _('(COPY)'))}
        new_tag = self.copy(default)
        for course in self.tag_course_ids:
            course.slide_channel_id.tag_ids = [(4, new_tag.id)]
        new_tag.bring_courses()
        action = self.env.ref(
            'website_slides.slide_channel_tag_action').read()[0]
        return action
