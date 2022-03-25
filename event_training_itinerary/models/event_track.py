# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventTrack(models.Model):
    _inherit = 'event.track'

    training_itinerary_id = fields.Many2one(
        string='Training itinerary', comodel_name='slide.channel.tag',
        related='event_id.training_itinerary_id', store=True)
    training_itinerary_courses_count = fields.Integer(
        string='Itinerary courses number', store=True,
        related='training_itinerary_id.courses_count')

    def button_show_event_itinerary_courses(self):
        self.ensure_one()
        if self.training_itinerary_courses_count > 0:
            action = self.env.ref(
                'event_training_itinerary.slide_channel_tag_course_action')
            action_dict = action and action.read()[0]
            action_dict["context"] = safe_eval(
                action_dict.get("context", "{}"))
            action_dict['context'].update({
                'default_slide_channel_tag_id': self.training_itinerary_id.id,
                'search_default_slide_channel_tag_id':
                self.training_itinerary_id.id})
            domain = expression.AND([
                [("slide_channel_tag_id", "=", self.training_itinerary_id.id)],
                safe_eval(action.domain or "[]")])
            action_dict.update({"domain": domain})
            return action_dict
