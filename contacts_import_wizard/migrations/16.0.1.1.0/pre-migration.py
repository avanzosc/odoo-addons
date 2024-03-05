# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "res_partner", "trade_name"):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE res_partner
            SET comercial = trade_name
            WHERE comercial is null;
            """,
        )
