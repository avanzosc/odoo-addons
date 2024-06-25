from datetime import datetime

from odoo import http
from odoo.http import request

from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlides(WebsiteSlides):
    @http.route()
    def slides_channel_all(self, slide_type=None, my=False, **post):
        res = super().slides_channel_all(slide_type, my, **post)
        user = request.env["res.users"].sudo().browse(request.uid)
        partner = user.partner_id
        today = datetime.today()
        registrations = (
            request.env["event.registration"]
            .sudo()
            .search(
                ["|", ("partner_id", "=", partner.id), ("student_id", "=", partner.id)]
            )
        )
        events = (
            request.env["event.event"]
            .sudo()
            .search(
                [
                    ("registration_ids", "in", registrations.ids),
                    "|",
                    ("date_begin", "=", False),
                    ("date_begin", "<=", today),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">", today),
                ]
            )
        )
        channel = res.qcontext.get("channels", False)
        channel_partner_ids = None
        if channel:
            today = datetime.today()
            channel_partner_ids = (
                request.env["slide.channel.partner"]
                .sudo()
                .search(
                    [
                        ("id", "in", channel.sudo().channel_partner_ids.ids),
                        "|",
                        ("real_date_start", "=", False),
                        ("real_date_start", "<=", today),
                        "|",
                        ("real_date_end", "=", False),
                        ("real_date_end", ">=", today),
                    ]
                )
            )
        res.qcontext.update(
            {"events": events, "channel_partner_ids": channel_partner_ids}
        )
        return res
