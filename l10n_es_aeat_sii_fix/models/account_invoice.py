# -*- coding: utf-8 -*-
# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _get_sii_invoice_dict_in(self, cancel=False):
        """Build dict with data to send to AEAT WS for invoice types:
        in_invoice and in_refund.

        :param cancel: It indicates if the dictionary if for sending a
          cancellation of the invoice.
        :return: invoices (dict) : Dict XML with data for this invoice.
        """
        self.ensure_one()
        inv_dict = super(AccountInvoice, self)._get_sii_invoice_dict_in(
            cancel=cancel)
        if any([self.sii_registration_key.code == '13',
                self.sii_registration_key_additional1.code == '13',
                self.sii_registration_key_additional2.code == '13']):
            inv_dict['FacturaRecibida'].update({
                'CuotaDeducible': 0,
            })
        return inv_dict
