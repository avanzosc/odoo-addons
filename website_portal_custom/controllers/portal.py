from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    @route()
    def home(self, **kw):
        res = super(CustomerPortal, self).home(**kw)
        user_id = request.env['res.users'].browse(request.uid)
        allowed_urls = user_id.company_id.portal_custom_entry_show
        res.qcontext.update({
            'allowed_urls': allowed_urls.mapped('url')
        })
        return res
