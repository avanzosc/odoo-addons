# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.constrains('supplier_invoice_number', 'period_id')
    def _check_unique_supplier_invoice_number_insensitive(self):
        if not self.period_id:
            super(AccountInvoice,
                  self)._check_unique_supplier_invoice_number_insensitive()
        else:
            if (self.supplier_invoice_number and
                    self.type in ('in_invoice', 'in_refund')):
                cond = [
                    ('commercial_partner_id', '=',
                     self.commercial_partner_id.id),
                    ('type', 'in', ('in_invoice', 'in_refund')),
                    ('supplier_invoice_number', '=ilike',
                     self.supplier_invoice_number),
                    ('id', '!=', self.id),
                    ('period_id', 'in',
                     self.period_id.fiscalyear_id.period_ids.ids)]
                invoices = self.search(cond)
                if invoices:
                    raise ValidationError(
                        _("The invoice/refund with supplier invoice number "
                          "'%s' already exists in Odoo under the number '%s' "
                          "for supplier '%s', and fiscal year.") % (
                            invoices[0].supplier_invoice_number,
                            invoices[0].number or '-',
                            invoices[0].partner_id.display_name))
