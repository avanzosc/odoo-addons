# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _prepare_tax_line_vals(self, line, tax):
        vals = super(AccountInvoice, self)._prepare_tax_line_vals(line, tax)
        if line.payment_percentage:
            percentage = line.payment_percentage / 100
            vals.update({
                'base': vals['base'] * percentage,
                'amount': vals['amount'] * percentage,
            })
        return vals
