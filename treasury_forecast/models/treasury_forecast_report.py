from odoo import fields, models


class TreasuryForecastReport(models.Model):
    _name = "treasury.forecast.report"
    _description = "Treasury Forecast Report"
    _auto = False

    date = fields.Date()
    partner_id = fields.Many2one("res.partner", string="Partner")
    product_id = fields.Many2one("product.product", string="Product")
    product_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        readonly=True,
    )
    name = fields.Char(string="Description")
    journal_id = fields.Many2one("account.journal", string="Journal")
    estimated_journal_id = fields.Many2one(
        "account.journal",
        string="Estimated Journal",
    )
    currency_id = fields.Many2one("res.currency", string="Currency")
    debit = fields.Monetary(string="Income", currency_field="currency_id")
    credit = fields.Monetary(string="Expense", currency_field="currency_id")
    balance = fields.Monetary(currency_field="currency_id")
    residual = fields.Monetary(currency_field="currency_id")
    source = fields.Selection(
        [("forecast", "Forecast"), ("move_line", "Move Line")],
        string="Origin",
    )
    financing_id = fields.Many2one("treasury.financing", string="Financing")

    category_id = fields.Many2one("treasury.financing.category", string="Category")

    parent_category_id = fields.Many2one(
        "treasury.financing.category", string="Parent Category"
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
                self._select_account(),
                self._from_account(),
                self._where_account(),
            ),
        ]

    def _select_forecast(self):
        select_ = """
            row_number() OVER() AS id,
            tf.date::date AS date,
            tf.partner_id AS partner_id,
            tf.product_id AS product_id,
            tf.product_category_id as product_category_id,
            tf.name AS name,
            tf.income AS debit,
            tf.expense AS credit,
            (tf.income - tf.expense) AS balance,
            (tf.income - tf.expense) AS residual,
            tf.journal_id AS journal_id,
            tf.journal_id AS estimated_journal_id,
            tf.currency_id AS currency_id,
            tf.financing_id AS financing_id,
            tf.category_id AS category_id,
            tf.parent_category_id AS parent_category_id,
            'forecast'::text AS source
        """
        additional_fields = self._select_additional_fields()
        for field_name, sql_expression in additional_fields.items():
            select_ += f""",
            {sql_expression} AS {field_name}
            """
        return select_

    def _from_forecast(self):
        return """
            treasury_forecast tf
        """

    def _where_forecast(self):
        return """
            tf.active = true
        """

    def _select_account(self):
        select_ = """
            row_number() OVER() + 1000000 AS id,
            aml.date_maturity::date AS date,
            aml.partner_id AS partner_id,
            aml.product_id AS product_id,
            aml.product_category_id as product_category_id,
            aml.name AS name,
            aml.debit AS debit,
            aml.credit AS credit,
            aml.balance AS balance,
            aml.amount_residual AS residual,
            aml.journal_id AS journal_id,
            am.estimated_journal_id AS estimated_journal_id,
            aml.currency_id AS currency_id,
            NULL AS financing_id,
            NULL AS category_id,
            NULL AS parent_category_id,
            'move_line'::text AS source
        """
        additional_fields = self._select_additional_fields()
        for field_name, sql_expression in additional_fields.items():
            select_ += f""",
            {sql_expression} AS {field_name}
            """
        return select_

    def _from_account(self):
        return """
            account_move_line aml
                JOIN account_move am ON am.id = aml.move_id
                JOIN account_account aa ON aa.id = aml.account_id
        """

    def _where_account(self):
        return """
            aml.date_maturity IS NOT NULL
              AND am.state = 'posted'
              AND aa.reconcile = TRUE
              AND (
                  aml.matching_number IS NULL
                  OR aml.amount_residual > 0
              )
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
