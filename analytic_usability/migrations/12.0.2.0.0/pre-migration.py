# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='account_analytic_account'
        AND column_name='user_id'
        """)
    if not cr.fetchone():
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE account_analytic_account
            ADD COLUMN user_id integer;
            """)
    openupgrade.logged_query(
        env.cr, """
        UPDATE account_analytic_account aa
        SET user_id = (SELECT user_id
                         FROM res_partner p
                        WHERE p.id = aa.partner_id
                          AND user_id IS NOT NULL)
        WHERE user_id IS NULL;
        """)
