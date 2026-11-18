# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    days_until_payment = fields.Float(
        readonly=True,
        aggregator="avg",
        digits=(16, 2),
    )

    @api.model
    def _select(self):
        return SQL(
            """
            %s,
            CASE
                WHEN move.days_until_payment_available
                    AND line.id = MIN(line.id) OVER (
                        PARTITION BY line.move_id
                    )
                THEN move.days_until_payment
                ELSE NULL
            END AS days_until_payment
            """,
            super()._select(),
        )
