# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EventEvent(models.Model):
    _inherit = "event.event"

    count_statistics = fields.Integer(
        string="Courses statistics",
        compute="_compute_count_statistics",
        compute_sudo=True,
    )

    def _compute_count_statistics(self):
        slide_partner_obj = self.env["slide.slide.partner"]
        for event in self:
            slide_partners = slide_partner_obj
            registrations = event.registration_ids.filtered(lambda x: x.student_id)
            if registrations:
                partners = registrations.mapped("student_id")
                cond = [
                    ("channel_id", "in", event.slides_ids.ids),
                    ("partner_id", "in", partners.ids),
                ]
                slide_partners = slide_partner_obj.search(cond)
            event.count_statistics = len(slide_partners)

    def button_show_slide_slide_partner(self):
        self.ensure_one()
        slide_partner_obj = self.env["slide.slide.partner"]
        registrations = self.registration_ids.filtered(lambda x: x.student_id)
        if registrations:
            partners = registrations.mapped("student_id")
            cond = [
                ("channel_id", "in", self.slides_ids.ids),
                ("partner_id", "in", partners.ids),
            ]
            slide_partners = slide_partner_obj.search(cond)
            if slide_partners:
                action = self.env["ir.actions.actions"]._for_xml_id(
                    "slide_partner_menu.action_slide_slide_partner"
                )
                domain = expression.AND(
                    [
                        [("id", "in", slide_partners.ids)],
                        safe_eval(action.get("domain") or "[]"),
                    ]
                )
                action.update(
                    {
                        "domain": domain,
                    }
                )
                return action
