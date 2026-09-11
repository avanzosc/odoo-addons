# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(
        self, grouped=False, final=False, date=None, start_date=None, end_date=None
    ):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)
        for invoice in invoices:
            vals = {}
            subscription_lines = invoice.invoice_line_ids.filtered(
                lambda line: line.subscription_id
                and line.deferred_start_date
                and line.deferred_end_date
            )
            if subscription_lines:
                vals = {
                    "start_date_period": min(
                        subscription_lines.mapped("deferred_start_date")
                    ),
                    "end_date_period": max(
                        subscription_lines.mapped("deferred_end_date")
                    ),
                }
                invoice.write(vals)
        return invoices
