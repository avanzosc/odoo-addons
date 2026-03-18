# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column purchase_price_unit for table stock_move")
    if not openupgrade.column_exists(cr, "stock_move", "purchase_price_unit"):
        cr.execute(
            """
            ALTER TABLE stock_move
            ADD COLUMN purchase_price_unit float;
            COMMENT ON COLUMN stock_move.purchase_price_unit
            IS 'Purchase Unit Price';
            """
        )

    _logger.info("Pre-creating column purchase_price_subtotal for table stock_move")
    if not openupgrade.column_exists(cr, "stock_move", "purchase_price_subtotal"):
        cr.execute(
            """
            ALTER TABLE stock_move
            ADD COLUMN purchase_price_subtotal float;
            COMMENT ON COLUMN stock_move.purchase_price_subtotal
            IS 'Purchase Subtotal';
            """
        )

    _logger.info("Pre-computing column purchase_price_unit for table stock_move")
    cr.execute(
        """
        UPDATE stock_move
        set    purchase_price_unit = (
                         SELECT purchase_order_line.price_unit
                         FROM   purchase_order_line
                         WHERE  purchase_order_line.id = stock_move.purchase_line_id
                         )
        WHERE  purchase_line_id is not null
    """
    )

    _logger.info("Pre-computing purchase_price_subtotal for table stock_move")
    cr.execute(
        """
        UPDATE stock_move
        set    purchase_price_subtotal = purchase_price_unit * product_uom_qty
        WHERE  purchase_price_unit is not null
          AND  product_uom_qty is not null
    """
    )
