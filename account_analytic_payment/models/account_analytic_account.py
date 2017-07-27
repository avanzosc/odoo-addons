# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.model
    def _prepare_invoice_data(self, contract):
        res = super(AccountAnalyticAccount,
                    self)._prepare_invoice_data(contract)
        partner = self.env['res.partner'].browse(res.get('partner_id', False))
        sale = self.env['sale.order'].search(
            [('project_id', '=', contract.id)])
        payment = sale and sale.payment_mode_id or \
            partner.customer_payment_mode
        res['payment_mode_id'] = payment.id
        res['partner_bank_id'] = payment.bank_id.id
        res['payment_term'] = sale and sale.payment_term.id or \
            partner.property_payment_term.id
        return res


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.multi
    def invoice_cost_create(self, data=None):
        invoice_ids = super(AccountAnalyticLine,
                            self).invoice_cost_create(data=data)
        for invoice in self.env['account.invoice'].browse(invoice_ids):
            partner = invoice.partner_id
            invoice.write({
                'payment_mode_id': partner.customer_payment_mode.id,
                'partner_bank_id': partner.customer_payment_mode.bank_id.id,
                'payment_term': partner.property_payment_term.id,
                })
        return invoice_ids
