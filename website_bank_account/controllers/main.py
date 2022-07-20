
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.addons.website.controllers.main import QueryURL


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
            is_unique, bank_ids = self.is_unique_account(data.get('bank_acc'))
            if not is_unique:
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
        acc = sanitize_account_number(account)
        bank_ids = request.env['res.partner.bank'].sudo().search([
            '|',
            ('acc_number', '=', acc),
            ('sanitized_acc_number', '=', acc)
        ])
        if bank_ids:
            return False, bank_ids
        return True, bank_ids

    def create_iban_account(self, account, partner):
        ctx = False
        bank_obj = request.env['res.partner.bank']
        # Check if account in partner accounts
        is_unique, bank_ids = self.is_unique_account(account)
        if is_unique:
            acc_type = bank_obj.retrieve_acc_type(account)
            if acc_type == 'iban':
                bank_obj.sudo().create({
                    'partner_id': partner.id,
                    'acc_number': account.upper(),
                })
                ctx = True
        return ctx

    @http.route()
    def address(self, **kw):
        res = super(WebsiteSale, self).address(**kw)
        order = res.qcontext.get('website_sale_order')
        user = request.env['res.users'].browse(request.session.uid)
        partner = order.partner_id if order else user.partner_id

        acquirer_id = kw.get('acquirer_id')
        partner_id = kw.get('partner_id')

        values = res.qcontext
        if partner:
            bank_ids = partner.bank_ids
            if bank_ids:
                values.update({'bank_acc_nr': bank_ids[0].acc_number})

        keep = QueryURL('/shop/address', partner_id=partner_id,
                            acquirer_id=acquirer_id)
        values.update({
            'keep': keep
        })
        res.qcontext.update(values)
        return res
