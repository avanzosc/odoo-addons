# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TreasuryForecastProjectReport(models.Model):
    _name = "treasury.forecast.project.report"
    _inherit = "treasury.forecast.report"
    _description = "Treasury Forecast Project Report"
    _auto = False

    source = fields.Selection(
        [("project", "Project")],
        string="Origin",
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
    )

    def _with(self):
        return ""

    def _select_additional_fields(self):
        return {}

    def _query_parts(self):
        return [
            (
                self._select_forecast(),
                self._from_forecast(),
                self._where_forecast(),
            ),
            (
                self._select_project(),
                self._from_project(),
                self._where_project(),
            ),
        ]

    def _select_forecast(self):
        select_ = super()._select_forecast()

        select_ = select_.replace(
            "'forecast'::text AS source",
            """
            'forecast'::text AS source,
            tf.analytic_account_id AS analytic_account_id
            """,
        )
        return select_

    def _select_project(self):
        select_ = """
            row_number() OVER() + 1000000 AS id,
            al.date::date AS date,
            al.partner_id AS partner_id,
            al.product_id AS product_id,
            al.product_category_id AS product_category_id,
            al.name AS name,
            GREATEST(al.amount, 0) AS debit,
            GREATEST(-al.amount, 0) AS credit,
            al.amount AS balance,
            0 AS residual,
            NULL AS journal_id,
            NULL AS estimated_journal_id,
            al.currency_id AS currency_id,
            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,
            'project'::text AS source,
            al.account_id AS analytic_account_id
        """
        additional_fields = self._select_additional_fields()
        for field_name, sql_expression in additional_fields.items():
            select_ += f""",
            {sql_expression} AS {field_name}
            """
        return select_

    def _from_project(self):
        return """
            account_analytic_line al
        """

    def _where_project(self):
        return """
            1 = 1
        """

    def _query(self):
        with_clause = self._with()
        unions = []
        for select_, from_, where_ in self._query_parts():
            unions.append(
                f"""
                (
                    SELECT
                        {select_}
                    FROM
                        {from_}
                    WHERE
                        {where_}
                )
                """
            )
        return f"""
            {"WITH " + with_clause if with_clause else ""}
            {" UNION ALL ".join(unions)}
        """

    @property
    def _table_query(self):
        return self._query()
