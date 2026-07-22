# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TreasuryForecastReport(models.Model):
    _inherit = "treasury.forecast.report"

    source = fields.Selection(
        selection_add=[("committed", "Committed")],
        ondelete={"committed": "set null"},
    )

    def _query_parts(self):
        res = super()._query_parts()
        res.append(
            (
                self._select_purchase(),
                self._from_purchase(),
                self._where_purchase(),
            )
        )
        return res

    def _select_purchase(self):
        return """
            row_number() OVER() + 2000000 AS id,

            po.date_approve::date AS date,
            pol.partner_id AS partner_id,
            pol.product_id AS product_id,
            pol.product_category_id AS product_category_id,

            pol.name AS name,
            CASE
               WHEN pol.price_subtotal < 0 THEN -pol.price_subtotal
               ELSE 0
            END AS debit,

            CASE
               WHEN pol.price_subtotal > 0 THEN pol.price_subtotal
               ELSE 0
            END AS credit,

            -pol.price_subtotal AS balance,
            -pol.price_subtotal AS residual,

            NULL AS journal_id,
            NULL AS estimated_journal_id,
            pol.currency_id AS currency_id,

            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,

            'committed'::text AS source
        """

    def _from_purchase(self):
        return """
           purchase_order_line pol
           JOIN purchase_order po ON po.id = pol.order_id
        """

    def _where_purchase(self):
        return """
           po.state IN ('purchase', 'done')
        """
