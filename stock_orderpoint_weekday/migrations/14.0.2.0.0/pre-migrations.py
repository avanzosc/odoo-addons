# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_warehouse_orderpoint_weekday
           SET weekday = Null
         WHERE type_update != 'weekday'
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_warehouse_orderpoint_weekday
           SET specific_day = Null
         WHERE type_update != 'specific'
        """,
    )
