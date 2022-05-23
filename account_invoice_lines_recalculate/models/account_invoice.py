# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    product_discount_percentage = fields.Float(
        related="product_id.discount_percentage")
    product_exclude_discount_categ = fields.Boolean(
        related="product_id.categ_id.discounts_exclude")
    invoice_state = fields.Selection(
        related="invoice_id.state", readonly=True
    )

    @api.multi
    def recalculate_invoice_line(self):
        for invoice_line in self:
            subtotal = sum(invoice_line.invoice_id.invoice_line_ids.filtered(
                lambda x: not x.product_id.categ_id.discounts_exclude and
                x.product_id.discount_percentage == 0).mapped(
                'price_subtotal'))
            discount_percentage = invoice_line.product_id.discount_percentage
            exclude = invoice_line.product_id.categ_id.discounts_exclude
            if exclude and discount_percentage > 0:
                invoice_line.price_unit = subtotal * (
                    discount_percentage / 100) * -1
            invoice_line.invoice_id._onchange_invoice_line_ids()
            invoice_line.invoice_id._onchange_cash_rounding()
