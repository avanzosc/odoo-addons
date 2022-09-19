# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(
        self, grouped=False, final=False, date=None, start_date=None, end_date=None
    ):
        invoices = super(SaleOrder, self)._create_invoices(
            grouped=grouped,
            final=final,
            date=date,
            start_date=start_date,
            end_date=end_date,
        )
        for invoice in invoices:
            for line in invoice.invoice_line_ids.filtered(
                lambda x: x.quantity != x.quantity2 and x.calculated_quantity2
            ):
                invoice.invoice_line_ids = [(1, line.id, {"quantity": line.quantity2})]
        return invoices
