# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.column_exists(cr, "stock_move_line", "cleaned_date"):
        cr.execute(
            """
            ALTER TABLE stock_move_line
            ADD COLUMN cleaned_date date;
            """
        )
        cr.execute(
            """
        update stock_move_line
        set    cleaned_date = (select stock_picking_batch.cleaned_date
                               from   stock_picking,
                                      stock_picking_batch
                               where  stock_picking.id = stock_move_line.picking_id
                                 and  stock_picking.batch_id is not null
                                 and  stock_picking_batch.id = stock_picking.batch_id)
        where  picking_id is not null;
            """
        )
        cr.execute(
            """
        update stock_move_line
        set    cleaned_date = (select stock_picking_batch.cleaned_date
                               from   stock_move,
                                      stock_inventory,
                                      stock_picking_batch
                               where  stock_move.id = stock_move_line.move_id
                                 and  stock_move.inventory_id is not null
                                 and  stock_inventory.id = stock_move.inventory_id
                                 and  stock_inventory.batch_id is not null
                                 and  stock_picking_batch.id = stock_inventory.batch_id)
        where  picking_id is null
          and  move_id is not null
            """
        )
