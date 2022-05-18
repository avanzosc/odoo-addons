
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    # @http.route()
    # def checkout(self, **post):
    #     order = request.website.sale_get_order()
    #     if not order.partner_id.bank_ids:
    #         return request.redirect(
    #             '/shop/address?partner_id=' + str(order.partner_id.id))
    #
    #     return super(WebsiteSale, self).checkout(**post)

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super(WebsiteSale, self).checkout_form_validate(
            mode, all_form_values, data)

        user = request.env['res.users'].browse(request.session.uid)
        partner = user.partner_id

        # account validation
        if data.get('bank_acc'):
            if not self.is_unique_account(
                    data.get('bank_acc') and not partner.bank_ids):
                error["bank_acc"] = 'error'
                error_message.append(
                    _('Invalid Bank Account! Bank account already registered.')
                )
            if not self.create_iban_account(data.get('bank_acc'), partner):
                error["bank_acc"] = 'error'
                error_message.append(
                    _('Invalid Bank Account! Bank number must be IBAN.'))

        return error, error_message

    def is_unique_account(self, account):
        bank_ids = request.env['res.partner.bank'].sudo().search([])
        for bank in bank_ids:
            if account == bank.acc_number:
                return False
        return True

    def create_iban_account(self, account, partner):
        bank_obj = request.env['res.partner.bank']
        # Check if account in partner accounts
        partner_bank_acc = bank_obj.sudo().search([
            ('partner_id', '=', partner.id),
            ('acc_number', '=', account)
        ])
        if not partner_bank_acc:
            acc_type = bank_obj.retrieve_acc_type(account)
            if acc_type == 'iban':
                bank_obj.sudo().create({
                    'partner_id': partner.id,
                    'acc_number': account.upper(),
                })
            else:
                return False
        return True

    @http.route()
    def address(self, **kw):
        res = super(WebsiteSale, self).address(**kw)
        order = res.qcontext.get('website_sale_order')
        user = request.env['res.users'].browse(request.session.uid)
        partner = order.partner_id if order else user.partner_id

        values = res.qcontext
        if partner:
            bank_ids = partner.bank_ids
            if bank_ids:
                values.update({'bank_acc_nr': bank_ids[0].acc_number})

        res.qcontext.update(values)
        return res
