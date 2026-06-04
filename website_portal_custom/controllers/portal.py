from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @route()
    def home(self, **kw):
        res = super().home(**kw)
        allowed_urls = request.env.user.company_id.portal_custom_entry_show
        res.qcontext.update({"allowed_urls": allowed_urls.mapped("url")})
        return res
