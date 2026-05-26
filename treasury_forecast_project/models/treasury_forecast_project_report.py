# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class TreasuryForecastProjectReport(models.Model):
    _name = "treasury.forecast.project.report"
    _inherit = "treasury.forecast.report"
    _description = "Treasury Forecast Project Report"
    _auto = False

    source = fields.Selection(
        [("forecast", "Forecast"), ("project", "Project")],
        string="Origin",
    )
    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
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
            tf.project_id AS project_id,
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
            aml.product_category_id AS product_category_id,
            al.name AS name,
            GREATEST(al.amount, 0) AS debit,
            GREATEST(-al.amount, 0) AS credit,
            al.amount AS balance,
            0 AS residual,
            am.journal_id AS journal_id,
            am.journal_id AS estimated_journal_id,
            al.currency_id AS currency_id,
            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,
            'project'::text AS source,
            CASE
                WHEN proj_count.cnt = 1 THEN pp.id
                ELSE NULL
            END AS project_id,
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
            LEFT JOIN account_move_line aml
                ON al.move_line_id = aml.id

            LEFT JOIN account_move am
                ON aml.move_id = am.id
            LEFT JOIN project_project pp
                ON pp.account_id = al.account_id
            LEFT JOIN (
                SELECT
                    account_id,
                    COUNT(*) AS cnt
                FROM project_project
                GROUP BY account_id
            ) proj_count
                ON proj_count.account_id = al.account_id
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
