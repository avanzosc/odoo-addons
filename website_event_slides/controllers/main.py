

from odoo import http
from odoo.http import request
from datetime import date
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlides(WebsiteSlides):

    @http.route()    
    def channel(self, channel, category=None, tag=None, page=1, slide_type=None
                , uncategorized=False, sorting=None, search=None, **kw):
        res = super(WebsiteSlides, self).channel(channel, category, tag,
                page, slide_type, uncategorized, sorting, search, **kw)
        user = request.env.user
        if not user._is_public():
            channel_partner = channel.sudo().channel_partner_ids.filtered(
                lambda r: r.partner_id.id == user.partner_id.id).sorted(
                'create_date')[:1]
            if channel_partner and not channel_partner.show_channel_partner:
                return request.redirect('/slides')

        return res
        
    @http.route()
    def slides_channel_home(self, **post):
        res = super(WebsiteSlides, self).slides_channel_home(**post)
        res_channels_my = res.qcontext.get('channels_my')
        if not request.env.user._is_public():
            domain = self.get_real_date_domain()
            domain += [('channel_id', 'in', res_channels_my.ids)]
            partner_channel_filtered = request.env[
                'slide.channel.partner'].sudo().search(domain).sorted(
                lambda channel: 0 if channel.completed else channel.completion,
                reverse=True)[:3]
            res.qcontext.update({
                'active_channels_my': partner_channel_filtered.mapped('channel_id')
            })
        return res

    def get_real_date_domain(self):
        return [
                    ('partner_id', '=', request.env.user.partner_id.id),
                    '|',
                    ('real_date_start', '<=', date.today()),
                    ('real_date_start', '=', False),
                    '|',
                    ('real_date_end', '>=', date.today()),
                    ('real_date_end', '=', False),
                ]
