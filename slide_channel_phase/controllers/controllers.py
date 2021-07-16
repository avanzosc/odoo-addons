
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_profile.controllers.main import WebsiteProfile


class WebsiteSlides(WebsiteProfile):

    def _get_channel_slides_base_domain(self, channel):
        base_domain = super(
            WebsiteSlides, self)._get_channel_slides_base_domain(channel)
        if channel.content_view == 'phase':
            logged_user = request.env.user.sudo()
            show_slide_ids = logged_user.partner_id.get_partner_phase_slides(
                channel)
            if show_slide_ids:
                base_domain = expression.AND(
                    [base_domain, [('id', 'in', show_slide_ids.ids)]])
        return base_domain
