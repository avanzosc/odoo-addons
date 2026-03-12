from odoo import fields, models, tools


class TreasuryForecastReport(models.Model):
    _name = "treasury.forecast.report"
    _description = "Treasury Forecast Report"
    _auto = False

    date = fields.Date(string="Fecha")
    partner_id = fields.Many2one("res.partner", string="Partner")
    product_id = fields.Many2one("product.product", string="Product")
    name = fields.Char(string="Description")

    journal_id = fields.Many2one("account.journal", string="Journal")
    estimated_journal_id = fields.Many2one(
        "account.journal",
        string="Estimated Journal",
    )
    currency_id = fields.Many2one("res.currency", string="Currency")

    debit = fields.Monetary(string="Expense", currency_field="currency_id")
    credit = fields.Monetary(string="Income", currency_field="currency_id")
    balance = fields.Monetary(currency_field="currency_id")
    residual = fields.Monetary(currency_field="currency_id")

    source = fields.Selection(
        [("forecast", "Forecast"), ("move_line", "Move Line")],
        string="Origen",
    )
    financing_id = fields.Many2one("treasury.financing", string="Financing")

    category_id = fields.Many2one("treasury.financing.category", string="Category")

    parent_category_id = fields.Many2one(
        "treasury.financing.category", string="Parent Category"
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW treasury_forecast_report AS (

                SELECT
                    row_number() OVER() AS id,
                    tf.date::date AS date,
                    tf.partner_id AS partner_id,
                    tf.product_id AS product_id,
                    tf.name AS name,
                    tf.expense AS debit,
                    tf.income AS credit,
                    (tf.income - tf.expense) AS balance,
                    (tf.income - tf.expense) AS residual,
                    tf.journal_id AS journal_id,
                    tf.journal_id AS estimated_journal_id,
                    tf.currency_id AS currency_id,
                    tf.financing_id AS financing_id,
                    tf.category_id AS category_id,
                    tf.parent_category_id AS parent_category_id,
                    'forecast'::text AS source
                FROM treasury_forecast tf
                WHERE tf.active = true

                UNION ALL

                SELECT
                    row_number() OVER() + 1000000 AS id,
                    aml.date_maturity::date AS date,
                    aml.partner_id AS partner_id,
                    aml.product_id AS product_id,
                    aml.name AS name,
                    CASE
                        WHEN am.move_type IN (
                            'in_invoice', 'in_refund') THEN aml.debit
                        ELSE 0.0
                    END AS debit,
                    CASE
                        WHEN am.move_type IN (
                            'out_invoice', 'out_refund') THEN aml.credit
                        ELSE 0.0
                    END AS credit,
                    CASE
                        WHEN am.move_type IN (
                            'in_invoice', 'in_refund') THEN aml.debit
                        WHEN am.move_type IN (
                            'out_invoice', 'out_refund') THEN aml.credit
                        ELSE 0.0
                    END AS balance,
                    aml.amount_residual AS residual,
                    aml.journal_id AS journal_id,
                    am.estimated_journal_id AS estimated_journal_id,
                    aml.currency_id AS currency_id,
                    NULL AS financing_id,
                    NULL AS category_id,
                    NULL AS parent_category_id,
                    'move_line'::text AS source
                FROM account_move_line aml
                JOIN account_move am ON am.id = aml.move_id
                WHERE aml.date_maturity IS NOT NULL
                  AND aml.amount_residual > 0
                  AND am.state = 'posted'
            )
        """)
