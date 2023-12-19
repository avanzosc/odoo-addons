# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_partner_bank_id(self, company_id):
        bank_obj = self.env['res.partner.bank']
        company = self.env['res.company'].browse(company_id)
        bank = super(AccountInvoice, self)._get_partner_bank_id(company_id)
        my_bank = False
        if company.partner_id:
            cond = [('partner_id', '=', company.partner_id.id),
                    ('company_id', '=', company.id),
                    ('currency_id', '=', company.currency_id.id)]
            my_bank = bank_obj.search(cond, limit=1)
        if my_bank:
            return my_bank
        return bank

    @api.onchange('currency_id')
    def onchange_currency_id(self):
        bank_obj = self.env['res.partner.bank']
        self.partner_bank_id = False
        if self.company_id.partner_id and self.currency_id:
            cond = [('partner_id', '=', self.company_id.partner_id.id),
                    ('company_id', '=', self.company_id.id),
                    ('currency_id', '=', self.currency_id.id)]
            my_bank = bank_obj.search(cond, limit=1)
            if my_bank:
                self.partner_bank_id = my_bank.id
