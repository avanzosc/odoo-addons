# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from psycopg2 import sql

_TABLES_WITH_GLOBAL_ORIGIN = (
    "sale_order",
    "purchase_order",
    "mrp_production",
    "stock_move",
    "stock_move_line",
)


def pre_init_hook(env):
    for table in _TABLES_WITH_GLOBAL_ORIGIN:
        env.cr.execute(
            sql.SQL(
                "ALTER TABLE {} ADD COLUMN IF NOT EXISTS global_origin VARCHAR"
            ).format(sql.Identifier(table))
        )
    env.cr.execute(
        """
        ALTER TABLE stock_move
        ADD COLUMN IF NOT EXISTS picking_type_sequence_code VARCHAR
        """
    )
    env.cr.execute(
        """
        UPDATE stock_move sm
        SET picking_type_sequence_code = spt.sequence_code
        FROM stock_picking_type spt
        WHERE spt.id = sm.picking_type_id
        """
    )
