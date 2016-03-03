# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def check_temporal(self):
        if self.invoice_line.filtered('temporal'):
            raise exceptions.Warning(_('The account is not assigned'))
        else:
            self.invoice_validate()
