

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route()
    def address(self, **kw):
        res = super(WebsiteSale, self).address(**kw)
        zip_obj = request.env['res.city.zip']
        zip_ids = zip_obj.search([])
        partner_id = res.qcontext.get('partner_id')
        logged_partner = request.env['res.partner'].browse(partner_id)
        partner_zip = logged_partner.zip_id
        partner_country = logged_partner.country_id
        if not partner_zip:
            partner_zip = zip_obj.search([('name', '=', logged_partner.zip)])
        if not partner_country:
            partner_country = request.env['res.country'].search([], limit=1)

        values = {
            'zip_ids': zip_ids,
            'partner_zip': partner_zip,
            'partner_country': partner_country
        }
        res.qcontext.update(values)
        return res

    @http.route(['/shop/address/update_json'], type='json', auth="public",
                methods=['POST'], website=True, csrf=False)
    def address_update_json(self, zip_str=None):
        values = {}
        if not zip_str or zip_str == '':
            return None
        zip_obj = request.env['res.city.zip']
        zip_id = zip_obj.search([('id', '=', int(zip_str))])
        city = zip_id.city_id
        country = city.country_id
        state = city.state_id
        values.update({
            'zip': zip_id.name,
            'city': city.name,
            'country': country.name,
            'country_id': country.id,
            'state': state.name,
            'state_id': state.id
        })
        return values
