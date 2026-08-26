# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TreasuryForecastProjectReport(models.Model):
    _inherit = "treasury.forecast.project.report"

    source = fields.Selection(
        selection_add=[("committed_sale", "Committed Sale")],
        ondelete={"committed_sale": "set null"},
    )

    def _query_parts(self):
        return super()._query_parts() + [
            (self._select_sale(), self._from_sale(), self._where_sale())
        ]

    def _pending_sale_subtotal(self):
        return """
            sol.price_subtotal
            * GREATEST(sol.product_uom_qty - sol.qty_invoiced, 0)
            / NULLIF(sol.product_uom_qty, 0)
        """

    def _select_sale(self):
        pending_subtotal = self._pending_sale_subtotal()
        return f"""
            row_number() OVER() + 3000000 AS id,
            so.date_order::date AS date,
            sol.order_partner_id AS partner_id,
            sol.product_id AS product_id,
            sol.name AS name,
            GREATEST({pending_subtotal}, 0)
                * analytic.percentage / 100 AS debit,
            GREATEST(-({pending_subtotal}), 0)
                * analytic.percentage / 100 AS credit,
            ({pending_subtotal}) * analytic.percentage / 100 AS balance,
            NULL AS journal_id,
            linked_project.id AS project_id,
            analytic.account_id AS analytic_account_id,
            NULL AS estimated_journal_id,
            sol.currency_id AS currency_id,
            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,
            product_template.categ_id AS product_category_id,
            'committed_sale'::text AS source
        """

    def _from_sale(self):
        return """
            sale_order_line sol
            JOIN sale_order so ON so.id = sol.order_id
            LEFT JOIN product_product product
                ON product.id = sol.product_id
            LEFT JOIN product_template product_template
                ON product_template.id = product.product_tmpl_id
            LEFT JOIN project_project line_project ON line_project.id = sol.project_id
            JOIN LATERAL (
                SELECT
                    account_id::integer AS account_id,
                    percentage::numeric AS percentage
                FROM jsonb_each_text(sol.analytic_distribution)
                    AS distribution(key, percentage)
                CROSS JOIN LATERAL unnest(string_to_array(distribution.key, ','))
                    AS account(account_id)
                UNION ALL
                SELECT
                    line_project.account_id,
                    100::numeric
                WHERE COALESCE(sol.analytic_distribution, '{}'::jsonb) = '{}'::jsonb
                  AND line_project.account_id IS NOT NULL
            ) AS analytic ON TRUE
            JOIN project_project linked_project
                ON linked_project.account_id = analytic.account_id
        """

    def _where_sale(self):
        return """
            so.state IN ('sale', 'done')
            AND sol.product_uom_qty > sol.qty_invoiced
        """
