# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TreasuryForecastProjectReport(models.Model):
    _inherit = "treasury.forecast.project.report"

    source = fields.Selection(
        selection_add=[("committed_purchase", "Committed Purchase")],
        ondelete={"committed_purchase": "set null"},
    )

    def _query_parts(self):
        return super()._query_parts() + [
            (self._select_purchase(), self._from_purchase(), self._where_purchase())
        ]

    def _pending_purchase_subtotal(self):
        return """
            pol.price_subtotal
            * GREATEST(pol.product_qty - pol.qty_invoiced, 0)
            / NULLIF(pol.product_qty, 0)
        """

    def _select_purchase(self):
        pending_subtotal = self._pending_purchase_subtotal()
        return f"""
            row_number() OVER() + 2000000 AS id,
            po.date_approve::date AS date,
            pol.partner_id AS partner_id,
            pol.product_id AS product_id,
            pol.name AS name,
            GREATEST(-({pending_subtotal}), 0)
                * distribution.percentage / 100 AS debit,
            GREATEST({pending_subtotal}, 0)
                * distribution.percentage / 100 AS credit,
            -({pending_subtotal})
                * distribution.percentage / 100 AS balance,
            NULL AS journal_id,
            linked_project.id AS project_id,
            distribution.account_id AS analytic_account_id,
            NULL AS estimated_journal_id,
            pol.currency_id AS currency_id,
            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,
            product_template.categ_id AS product_category_id,
            'committed_purchase'::text AS source
        """

    def _from_purchase(self):
        return """
            purchase_order_line pol
            JOIN purchase_order po ON po.id = pol.order_id
            LEFT JOIN product_product product
                ON product.id = pol.product_id
            LEFT JOIN product_template product_template
                ON product_template.id = product.product_tmpl_id
            JOIN LATERAL (
                SELECT
                    account_id::integer AS account_id,
                    percentage::numeric AS percentage
                FROM jsonb_each_text(pol.analytic_distribution)
                    AS item(key, percentage)
                CROSS JOIN LATERAL unnest(string_to_array(item.key, ','))
                    AS account(account_id)
            ) AS distribution ON TRUE
            JOIN project_project linked_project
                ON linked_project.account_id = distribution.account_id
        """

    def _where_purchase(self):
        return """
            po.state IN ('purchase', 'done')
            AND pol.product_qty > pol.qty_invoiced
        """
