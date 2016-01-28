# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def check_temporal(self):
        for line in self.invoice_line:
            if line.temporal:
                raise exceptions.Warning(_('The account is not assigned'))
            else:
                self.invoice_validate()
