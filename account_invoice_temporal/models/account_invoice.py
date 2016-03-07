# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _compute_is_temporal(self):
        for invoice in self:
            invoice.is_temporal = invoice.invoice_line.filtered('temporal')

    is_temporal = fields.Boolean(compute=_compute_is_temporal)

    @api.multi
    def check_temporal(self):
        if self.invoice_line.filtered('temporal'):
            raise exceptions.Warning(_('The account is not assigned'))
        else:
            self.signal_workflow('invoice_open')
