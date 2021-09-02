
from odoo import http
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventController(WebsiteEventController):

    @http.route()
    def event_register(self, event, **post):
        res = super(WebsiteEventController, self).event_register(event, **post)
        logged_partner = request.env.user.sudo().partner_id
        res.qcontext.update({
            'logged_partner': logged_partner
        })
        return res
