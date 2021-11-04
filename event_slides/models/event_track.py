# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventTrack(models.Model):
    _inherit = "event.track"

    count_courses = fields.Integer(
        string='Courses',
        compute='_compute_count_courses',
        compute_sudo=True)

    def _compute_count_courses(self):
        for track in self:
            track.count_courses = len(track.sudo().event_id.slides_ids)

    def button_show_event_courses(self):
        self.ensure_one()
        if self.count_courses > 0:
            action = self.env.ref(
                'website_slides.slide_channel_action_overview')
            action_dict = action and action.read()[0]
            action_dict["context"] = safe_eval(
                action_dict.get("context", "{}"))
            action_dict['context'].update({
                'default_event_id': self.event_id.id,
                'search_default_event_id': self.event_id.id})
            domain = expression.AND([
                [("id", "in", self.event_id.slides_ids.ids)],
                safe_eval(action.domain or "[]")])
            action_dict.update({"domain": domain})
            return action_dict
