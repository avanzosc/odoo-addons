# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        result = super(AccountInvoice, self).action_invoice_open()
        for invoice in self.filtered(
                lambda x: x.state == "open" and x.type == "in_invoice"):
            for line in invoice.invoice_line_ids:
                line.mapped('product_id').set_product_last_supplier_invoice(
                    invoice.id)
        return result

    @api.multi
    def action_invoice_cancel(self):
        result = super(AccountInvoice, self).action_invoice_cancel()
        for invoice in self.filtered(
                lambda x: x.state == "cancel" and x.type == "in_invoice"):
            for line in invoice.invoice_line_ids:
                line.mapped('product_id').set_product_last_supplier_invoice()
        return result
