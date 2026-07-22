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
                self._select_sale(),
                self._from_sale(),
                self._where_sale(),
            )
        )
        return res

    def _select_sale(self):
        return """
           row_number() OVER() + 3000000 AS id,

           so.date_order::date AS date,
           sol.order_partner_id AS partner_id,
           sol.product_id AS product_id,
           sol.product_category_id AS product_category_id,

           sol.name AS name,

            CASE
              WHEN sol.price_subtotal > 0 THEN sol.price_subtotal
              ELSE 0
            END AS debit,

            CASE
              WHEN sol.price_subtotal < 0 THEN -sol.price_subtotal
              ELSE 0
            END AS credit,

            sol.price_subtotal AS balance,
            sol.price_subtotal AS residual,

            NULL AS journal_id,
            NULL AS estimated_journal_id,
            sol.currency_id AS currency_id,
            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,

            'committed'::text AS source
        """

    def _from_sale(self):
        return """
            sale_order_line sol
            JOIN sale_order so ON so.id = sol.order_id
        """

    def _where_sale(self):
        return """
           so.state IN ('sale', 'done')
        """
