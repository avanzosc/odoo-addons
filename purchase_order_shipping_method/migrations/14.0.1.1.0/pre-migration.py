# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.column_exists(cr, "stock_picking", "total_done_qty"):
        cr.execute(
            """
            ALTER TABLE stock_picking
            ADD COLUMN total_done_qty float;
            """
        )
        cr.execute(
            """
            UPDATE stock_picking
            SET     total_done_qty = (SELECT SUM(qty_done)
                            FROM    stock_move_line
                            WHERE stock_move_line.picking_id = stock_picking.id)
            """
        )
