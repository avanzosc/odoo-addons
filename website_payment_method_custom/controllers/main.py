
from odoo import http, _
from odoo.http import request
from odoo.addons.website_bank_account.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    def checkout_check_iban_address(self, order, acquirer_id=None):
        if acquirer_id and len(order.partner_id.bank_ids.ids) == 0:
            return request.redirect(
                '/shop/address?partner_id=%d&acquirer_id=%s' % (
                    order.partner_id.id, acquirer_id.id))

    @http.route()
    def payment(self, **post):
        res = super(WebsiteSale, self).payment(**post)
        order = request.website.sale_get_order()
        acquirers = res.qcontext.get('acquirers')
        submit_txt = None
        if acquirers and len(acquirers) == 1:
            acquirer_id = acquirers[0]
            if acquirer_id.payment_mode_id and acquirer_id.payment_mode_id.sudo().payment_method_id.bank_account_required:
                redirection = self.checkout_check_iban_address(order, acquirer_id=acquirer_id)
                if redirection:
                    return redirection
            if acquirer_id.website_payment_btn_text != '':
                submit_txt = acquirer_id.website_payment_btn_text

        if submit_txt:
            res.qcontext.update({
                'submit_txt': submit_txt
            })
        return res

    @http.route()
    def address(self, **kw):
        res = super(WebsiteSale, self).address(**kw)
        required_list = 'phone,name'
        acquirer_id = kw.get('acquirer_id')
        vals = {}
        if acquirer_id and acquirer_id:
            required_list += ',bank_acc'
            vals.update({'acquirer_id': acquirer_id})
        vals.update({'required_list': required_list})
        res.qcontext.update(vals)
        return res
