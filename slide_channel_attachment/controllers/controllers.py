
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

        logged_partner = request.env.user.partner_id

        slide = request.env['slide.channel'].browse(int(slide_id))
        slide_slide_partner_obj = request.env['slide.slide.partner']
        slide_channel_partner = slide_slide_partner_obj.sudo().search([
            ('slide_id', '=', slide.id),
            ('partner_id', '=', logged_partner.id)
        ])

        values = {
            'slide': slide.id,
            'attachment': attachment,
        }

        attachment_obj = request.env['ir.attachment']
        new_attachment = attachment_obj.sudo().create({
            'datas': attachment.split('base64,')[1],
            'type': 'binary',
            'name': "%s %s.pdf" % (
                slide_channel_partner.slide_id.name, logged_partner.name),
            'res_id': slide_channel_partner.id,
            'res_model': slide_slide_partner_obj.sudo()._name,
        })

        return values
