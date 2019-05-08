# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    payment_percentage = fields.Float(string='Payment %', default=100.0)

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date',
                 'payment_percentage')
    def _compute_price(self):
        super(AccountInvoiceLine, self)._compute_price()
        if self.payment_percentage > 0 and self.payment_percentage != 100.0:
            if self.price_subtotal:
                self.price_subtotal = (
                    self.price_subtotal * self.payment_percentage) / 100
            if self.price_subtotal_signed:
                self.price_subtotal_signed = (
                    self.price_subtotal_signed * self.payment_percentage) / 100
            if self.price_total:
                self.price_total = (
                    self.price_total * self.payment_percentage) / 100
            for line in self.invoice_id.tax_line_ids:
                line.amount_total = (
                    line.amount_total * self.payment_percentage) / 100
            self.invoice_id._compute_amount()
