# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventTrack(models.Model):
    _inherit = 'event.track'

    count_statistics = fields.Integer(
        string='Courses statistics',
        compute='_compute_count_statistics',
        compute_sudo=True)

    def _compute_count_statistics(self):
        slide_partner_obj = self.env['slide.slide.partner']
        for track in self:
            slide_partners = slide_partner_obj
            date = self.date.date()
            registrations = self.event_id.registration_ids.filtered(
                lambda x: x.student_id and x.real_date_start and
                date >= x.real_date_start and
                (not x.real_date_end or
                 (x.real_date_end and date <= x.real_date_end)))
            if registrations:
                partners = registrations.mapped('student_id')
                cond = [('channel_id', 'in', track.event_id.slides_ids.ids),
                        ('partner_id', 'in', partners.ids)]
                slide_partners = slide_partner_obj.search(cond)
            track.count_statistics = len(slide_partners)

    def button_show_slide_slide_partner(self):
        slide_partner_obj = self.env['slide.slide.partner']
        self.ensure_one()
        if self.count_statistics > 0:
            action = self.env.ref(
                'slide_partner_menu.action_slide_slide_partner')
            action_dict = action and action.read()[0]
            action_dict["context"] = safe_eval(
                action_dict.get("context", "{}"))
            slide_partners = slide_partner_obj
            date = self.date.date()
            registrations = self.event_id.registration_ids.filtered(
                lambda x: x.student_id and x.real_date_start and
                date >= x.real_date_start and
                (not x.real_date_end or
                 (x.real_date_end and date <= x.real_date_end)))
            if registrations:
                partners = registrations.mapped('student_id')
                cond = [('channel_id', 'in', self.event_id.slides_ids.ids),
                        ('partner_id', 'in', partners.ids)]
                slide_partners = slide_partner_obj.search(cond)
                domain = expression.AND([
                    [("id", "in", slide_partners.ids)],
                    safe_eval(action.domain or "[]")])
                action_dict.update({"domain": domain})
                return action_dict
