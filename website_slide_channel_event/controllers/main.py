
from odoo.http import request
from odoo import http
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlides(WebsiteSlides):

    @http.route()
    def slides_channel_all(self, slide_type=None, my=False, **post):
        res = super(WebsiteSlides, self).slides_channel_all(slide_type, my, **post)
        user = request.env['res.users'].sudo().browse(request.uid)
        partner = user.partner_id
        registrations = request.env['event.registration'].sudo().search([
            '|',
            ('partner_id', '=', partner.id),
            ('student_id', '=', partner.id)
        ])
        events = request.env['event.event'].sudo().search([
            ('registration_ids', 'in', registrations.ids)
        ])
        res.qcontext.update({'events': events})
        return res
