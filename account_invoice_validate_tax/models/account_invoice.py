# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        for invoice in self:
            for line in invoice.invoice_line_ids.filtered(
                    lambda x: x.display_type not in ('line_section',
                                                     'line_note')):
                if not line.invoice_line_tax_ids:
                    message = _(u"You must introduce tax to the line with "
                                "description: {}").format(line.name)
                    raise ValidationError(message)
        return super(AccountInvoice, self).action_invoice_open()
