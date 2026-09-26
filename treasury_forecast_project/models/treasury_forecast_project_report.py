# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, tools


class TreasuryForecastProjectReport(models.Model):
    _name = "treasury.forecast.project.report"
    _description = "Treasury Forecast Project Report"
    _auto = False

    date = fields.Date()
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    name = fields.Char(string="Description")
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal")
    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
    )
    estimated_journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Estimated Journal",
    )
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    debit = fields.Monetary(string="Income", currency_field="currency_id")
    credit = fields.Monetary(string="Expense", currency_field="currency_id")
    balance = fields.Monetary(currency_field="currency_id")
    source = fields.Selection(
        [("forecast", "Forecast"), ("project", "Project")],
        string="Origin",
    )
    financing_id = fields.Many2one(
        comodel_name="treasury.financing", string="Financing"
    )
    category_id = fields.Many2one(
        comodel_name="treasury.financing.category", string="Category"
    )
    parent_category_id = fields.Many2one(
        comodel_name="treasury.financing.category", string="Parent Category"
    )
    product_category_id = fields.Many2one(
        string="Product Category", comodel_name="product.category"
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(f"CREATE OR REPLACE VIEW {self._table} AS ({self._query()});")

    def _query(self, with_=None, select=None, join=None, group_by=None):
        query = "\n".join(
            [
                self._with_clause(*(with_ or [])),
                self._select_clause(*(select or [])),
                self._from_clause(*(join or [])),
                self._group_by_clause(*(group_by or [])),
            ]
        )
        additional_queries = [
            f"SELECT {select_} FROM {from_} WHERE {where_}"
            for select_, from_, where_ in self._query_parts()
        ]
        return "\nUNION ALL\n".join([query, *additional_queries])

    def _query_parts(self):
        return []

    def _with_clause(self, *with_):
        # Extra clauses formatted as `cte1 AS (SELECT ...)`, `cte2 AS (SELECT ...)`...
        return (
            """
WITH
    """
            + ",\n    ".join(with_)
            if with_
            else ""
        )

    def _select_clause(self, *select):
        return """
SELECT
    row_number() OVER() AS id,
    tf.date::date AS date,
    tf.partner_id AS partner_id,
    tf.product_id AS product_id,
    tf.name AS name,
    tf.income AS debit,
    tf.expense AS credit,
    (tf.income - tf.expense) AS balance,
    tf.journal_id AS journal_id,
    tf.project_id As project_id,
    tf.analytic_account_id AS analytic_account_id,
    tf.journal_id AS estimated_journal_id,
    tf.currency_id AS currency_id,
    tf.financing_id AS financing_id,
    tf.category_id AS category_id,
    tf.parent_category_id AS parent_category_id,
    pt.categ_id AS product_category_id,
    'forecast'::text AS source
FROM treasury_forecast tf
LEFT JOIN product_product pp
    ON pp.id = tf.product_id
LEFT JOIN product_template pt
    ON pt.id = pp.product_tmpl_id
WHERE tf.active = true

UNION ALL

SELECT
    row_number() OVER() + 1000000 AS id,
    al.date::date AS date,
    al.partner_id AS partner_id,
    al.product_id AS product_id,
    al.name AS name,
    GREATEST(al.amount, 0) AS debit,
    GREATEST(-al.amount, 0) AS credit,
    al.amount AS balance,
    am.journal_id AS journal_id,
    CASE
        WHEN proj_count.cnt = 1 THEN pp.id
        ELSE NULL
    END AS project_id,
    al.account_id AS analytic_account_id,
    am.journal_id  AS estimated_journal_id,
    al.currency_id AS currency_id,
    NULL AS financing_id,
    NULL AS category_id,
    NULL AS parent_category_id,
    al.product_category_id as product_category_id,
    'project'::text AS source
FROM account_analytic_line al
LEFT JOIN account_move_line aml
    ON al.move_line_id = aml.id
LEFT JOIN account_move am
    ON aml.move_id = am.id
LEFT JOIN project_project pp
    ON pp.account_id = al.account_id
LEFT JOIN (
    SELECT account_id, COUNT(*) AS cnt
    FROM project_project
    GROUP BY account_id
) proj_count
    ON proj_count.account_id = al.account_id
""" + (",\n    " + ",\n    ".join(select) if select else "")

    def _from_clause(self, *join_):
        # Extra clauses formatted as `column1`, `column2`...
        return """
""" + ("\n".join(join_) + "\n" if join_ else "")

    def _group_by_clause(self, *group_by):
        # Extra clauses formatted like `column1`, `column2`...
        return (
            """
GROUP BY
    """
            + ",\n    ".join(group_by)
            if group_by
            else ""
        )
