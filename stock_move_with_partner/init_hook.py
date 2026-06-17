# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    stored_partner_in_stock_move(env.cr)
    stored_partner_in_stock_move_line(env.cr)


def stored_partner_in_stock_move(cr):
    cr.execute(
        """
        UPDATE stock_move
        set    partner_id = (SELECT stock_picking.partner_id
                             FROM   stock_picking
                             WHERE  stock_picking.id = stock_move.picking_id)
        WHERE  partner_id is null
          AND  picking_id is not null
    """
    )


def stored_partner_in_stock_move_line(cr):
    _logger.info("Pre-creating column partner_id for table stock_move_line")
    if not openupgrade.column_exists(cr, "stock_move_line", "partner_id"):
        cr.execute(
            """
            ALTER TABLE stock_move_line
            ADD COLUMN partner_id integer;
            COMMENT ON COLUMN stock_move_line.partner_id
            IS 'Destination Address';
            """
        )
    _logger.info("Pre-computing column partner_id for table stock_move_line")
    cr.execute(
        """
        UPDATE stock_move_line
        set    partner_id = (SELECT stock_move.partner_id
                             FROM   stock_move
                             WHERE  stock_move.id = stock_move_line.move_id
                         )
        WHERE  move_id is not null
    """
    )
