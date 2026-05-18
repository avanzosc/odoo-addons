from odoo import tools


def create_treasury_forecast_view(env):
    tools.drop_view_if_exists(env.cr, "treasury_forecast_report")

    env.cr.execute("""
        CREATE OR REPLACE VIEW treasury_forecast_report AS
        SELECT
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
        FROM treasury_forecast tf
        WHERE tf.active = true

        UNION ALL

        SELECT
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
        FROM account_move_line aml
        JOIN account_move am ON am.id = aml.move_id
        JOIN account_account aa ON aa.id = aml.account_id
        WHERE aml.date_maturity IS NOT NULL
          AND am.state = 'posted'
          AND aa.reconcile = TRUE
          AND (
              aml.matching_number IS NULL
              OR aml.amount_residual > 0
          )
    """)
