# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "stock_picking_emptying_expired", "expired_date"):
        openupgrade.add_fields(
            env,
            [
                (
                    "expired_date",
                    "stock.picking",
                    "stock_picking",
                    "datetime",
                    False,
                    "stock_picking_emptying_expired",
                ),
            ],
        )
    openupgrade.logged_query(
        env.cr,
        """UPDATE stock_picking
            SET expired_date = custom_date_done
        """,
    )
