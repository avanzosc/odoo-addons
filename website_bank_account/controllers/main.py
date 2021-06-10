
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route()
    def checkout(self, **post):
        order = request.website.sale_get_order()
        if not order.partner_id.bank_ids:
            return request.redirect(
                '/shop/address?partner_id=' + str(order.partner_id.id))

        return super(WebsiteSale, self).checkout(**post)

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super(WebsiteSale, self).checkout_form_validate(
            mode, all_form_values, data)

        user = request.env['res.users'].browse(request.session.uid)
        partner = user.partner_id

        # account validation
        if data.get('bank_acc') and not self.is_unique_account(
                data.get('bank_acc') and not partner.bank_ids):
            error["bank_acc"] = 'error'
            error_message.append(
                _('Invalid Bank Account! Bank account already registered.'))

        return error, error_message

    def is_unique_account(self, account):
        bank_ids = request.env['res.partner.bank'].sudo().search([])
        for bank in bank_ids:
            if account == bank.acc_number:
                return False
        return True

    @http.route()
    def address(self, **kw):
        bank_obj = request.env['res.partner.bank']
        res = super(WebsiteSale, self).address(**kw)
        order = res.qcontext.get('website_sale_order')
        user = request.env['res.users'].browse(request.session.uid)
        partner = order.partner_id if order else user.partner_id

        acc_error = False
        error = res.qcontext.get('error')
        if error and 'bank_acc' in error:
            acc_error = True
        values = {}
        if partner:
            bank_ids = partner.bank_ids
            if bank_ids:
                values.update({'bank_acc_nr': bank_ids[0].acc_number})
            if 'bank_acc' in kw and not bank_ids:
                bank_account = kw.get('bank_acc')
                partner_bank_acc = bank_obj.sudo().search([
                    ('partner_id', '=', partner.id),
                    ('acc_number', '=', bank_account)
                ])
                if not partner_bank_acc and not acc_error:
                    bank_obj.sudo().create({
                        'partner_id': partner.id,
                        'acc_number': bank_account,
                    })
        res.qcontext.update(values)
        return res
