
from odoo import http
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_profile.controllers.main import WebsiteProfile

class WebsiteSlides(WebsiteProfile):
    @http.route()
    def slide_view(self, slide, **kwargs):
        res = super(WebsiteSlides, self).slide_view(slide, **kwargs)
        base_url = '/slides/slide'
        keep = QueryURL(base_url, slide=slide)
        res.qcontext.update({
            'keep': keep
        })
        return res
