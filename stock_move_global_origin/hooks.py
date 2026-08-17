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


def pre_init_hook(cr):
    for table in _TABLES_WITH_GLOBAL_ORIGIN:
        cr.execute(
            sql.SQL(
                "ALTER TABLE {} ADD COLUMN IF NOT EXISTS global_origin VARCHAR"
            ).format(sql.Identifier(table))
        )
    cr.execute("ALTER TABLE stock_move_line ADD COLUMN IF NOT EXISTS origin VARCHAR")
    cr.execute("ALTER TABLE stock_move ADD COLUMN IF NOT EXISTS origin_display VARCHAR")
    cr.execute(
        "ALTER TABLE stock_move_line ADD COLUMN IF NOT EXISTS origin_display VARCHAR"
    )
    cr.execute(
        """
        UPDATE stock_move sm
        SET origin_display = COALESCE(
            NULLIF(sm.origin, ''),
            (
                SELECT so.name FROM sale_order_line sol
                JOIN sale_order so ON so.id = sol.order_id
                WHERE sol.id = sm.sale_line_id
            ),
            (
                SELECT po.name FROM purchase_order_line pol
                JOIN purchase_order po ON po.id = pol.order_id
                WHERE pol.id = sm.purchase_line_id
            ),
            (SELECT mp.name FROM mrp_production mp WHERE mp.id = sm.raw_material_production_id),
            (SELECT mp.name FROM mrp_production mp WHERE mp.id = sm.production_id)
        )
        WHERE sm.origin_display IS NULL
        """
    )
    cr.execute(
        """
        UPDATE stock_move_line sml
        SET origin_display = sm.origin_display
        FROM stock_move sm
        WHERE sm.id = sml.move_id AND sml.origin_display IS NULL
        """
    )
