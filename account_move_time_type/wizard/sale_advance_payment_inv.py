# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount)
        for line in invoice.invoice_line_ids.filtered(
                lambda x: x.quantity != x.quantity2):
            invoice.invoice_line_ids = [
                (1, line.id, {'quantity': line.quantity2})]
        return invoice
