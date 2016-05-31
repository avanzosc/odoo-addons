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
        payment = partner.customer_payment_mode
        res['payment_mode_id'] = payment.id
        res['partner_bank_id'] = payment.bank_id.id
        return res
