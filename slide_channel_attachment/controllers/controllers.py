
import unicodedata
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_profile.controllers.main import WebsiteProfile


class WebsiteSlides(WebsiteProfile):
    @http.route()
    def slide_view(self, slide, **kwargs):
        res = super(WebsiteSlides, self).slide_view(slide, **kwargs)
        keep = QueryURL(slide=slide)
        slide_channel_partner = request.env['slide.slide.partner'].sudo().search([
            ('slide_id', '=', slide.id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        res.qcontext.update({
            'keep': keep,
            'partner_slide': slide_channel_partner
        })
        return res

    @http.route(['/slides/save_attachment'], type='json', auth="public",
                methods=['POST'], website=True, csrf=False)
    def slide_view_json(self, slide_id, attachment):

        if not slide_id or not attachment:
            return False

        slide = request.env['slide.channel'].browse(int(slide_id))
        slide_channel_partner = request.env['slide.slide.partner'].sudo().search([
            ('slide_id', '=', slide.id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        if slide_channel_partner:
            slide_channel_partner.write({'slide_attachment': attachment})
        values = {
            'slide': slide.id,
            'attachment': attachment,
        }
        return values
