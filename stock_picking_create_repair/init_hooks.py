# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column is_repair for table sale_order")
    if not openupgrade.column_exists(cr, "sale_order", "is_repair"):
        cr.execute(
            """
            ALTER TABLE sale_order
            ADD COLUMN is_repair boolean;
            COMMENT ON COLUMN sale_order.is_repair
            IS 'It''s repair';
            """
        )
    _logger.info("Pre-creating column is_repair for table sale_order_line")
    if not openupgrade.column_exists(cr, "sale_order_line", "is_repair"):
        cr.execute(
            """
            ALTER TABLE sale_order_line
            ADD COLUMN is_repair boolean;
            COMMENT ON COLUMN sale_order_line.is_repair
            IS 'It''s repair';
            """
        )
    _logger.info("Pre-creating column is_repair for table stock_move")
    if not openupgrade.column_exists(cr, "stock_move", "is_repair"):
        cr.execute(
            """
            ALTER TABLE stock_move
            ADD COLUMN is_repair boolean;
            COMMENT ON COLUMN stock_move.is_repair
            IS 'It''s repair';
            """
        )
    _logger.info("Pre-creating column is_repair for table stock_move_line")
    if not openupgrade.column_exists(cr, "stock_move_line", "is_repair"):
        cr.execute(
            """
            ALTER TABLE stock_move_line
            ADD COLUMN is_repair boolean;
            COMMENT ON COLUMN stock_move_line.is_repair
            IS 'It''s repair';
            """
        )
    _logger.info("Pre-creating column is_repair for table account_move_line")
    if not openupgrade.column_exists(cr, "account_move_line", "is_repair"):
        cr.execute(
            """
            ALTER TABLE account_move_line
            ADD COLUMN is_repair boolean;
            COMMENT ON COLUMN account_move_line.is_repair
            IS 'It''s repair';
            """
        )
    _logger.info("Pre-creating column is_repair for table repair_order")
    if not openupgrade.column_exists(cr, "repair_order", "is_repair"):
        cr.execute(
            """
            ALTER TABLE repair_order
            ADD COLUMN is_repair boolean;
            COMMENT ON COLUMN repair_order.is_repair
            IS 'It''s repair';
            """
        )
