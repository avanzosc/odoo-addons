# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column sale_price_unit for table stock_move")
    if not openupgrade.column_exists(cr, "stock_move", "sale_price_unit"):
        cr.execute(
            """
            ALTER TABLE stock_move
            ADD COLUMN sale_price_unit float;
            COMMENT ON COLUMN stock_move.sale_price_unit
            IS 'Sale Unit Price';
            """
        )

    _logger.info("Pre-creating column sale_price_subtotal for table stock_move")
    if not openupgrade.column_exists(cr, "stock_move", "sale_price_subtotal"):
        cr.execute(
            """
            ALTER TABLE stock_move
            ADD COLUMN sale_price_subtotal float;
            COMMENT ON COLUMN stock_move.sale_price_subtotal
            IS 'Sale Subtotal';
            """
        )

    _logger.info("Pre-computing column sale_price_unit for table stock_move")
    cr.execute(
        """
        UPDATE stock_move
        set    sale_price_unit = (
                         SELECT sale_order_line.price_unit
                         FROM   sale_order_line
                         WHERE  sale_order_line.id = stock_move.sale_line_id
                         )
        WHERE  sale_line_id is not null
    """
    )

    _logger.info("Pre-computing sale_price_subtotal for table stock_move")
    cr.execute(
        """
        UPDATE stock_move
        set    sale_price_subtotal = sale_price_unit * product_uom_qty
        WHERE  sale_price_unit is not null
          AND  product_uom_qty is not null
    """
    )
