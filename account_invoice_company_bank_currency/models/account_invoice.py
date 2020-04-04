# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


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
