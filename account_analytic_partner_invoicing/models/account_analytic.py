# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _recurring_create_invoice(self, automatic=False):
        res = super(AccountAnalyticAccount,
                    self)._recurring_create_invoice(automatic=automatic)
        invoice_obj = self.env['account.invoice']
        for account in self:
            invoice = invoice_obj.browse(res)
            invoice.payment_mode_id = account.partner_id.customer_payment_mode
            invoice.partner_bank_id = (
                account.partner_id.customer_payment_mode.bank_id)
            invoice.payment_term = account.partner_id.property_payment_term
        return res
