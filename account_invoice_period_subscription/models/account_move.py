# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def put_subscription_dates(self):
        for invoice in self.filtered(
            lambda x: not x.start_date_period and not x.end_date_period
        ):
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
