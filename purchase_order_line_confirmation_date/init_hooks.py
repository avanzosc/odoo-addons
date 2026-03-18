# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column confirmation_date for table purchase_order_line")
    if not openupgrade.column_exists(cr, "purchase_order_line", "confirmation_date"):
        cr.execute(
            """
            ALTER TABLE purchase_order_line
            ADD COLUMN confirmation_date date;
            COMMENT ON COLUMN purchase_order_line.confirmation_date
            IS 'Confirmation Date';
            """
        )

    _logger.info(
        "Pre-creating column purchase_line_confirmation_date for table stock_move"
    )
    if not openupgrade.column_exists(
        cr, "stock_move", "purchase_line_confirmation_date"
    ):
        cr.execute(
            """
            ALTER TABLE stock_move
            ADD COLUMN purchase_line_confirmation_date date;
            COMMENT ON COLUMN stock_move.purchase_line_confirmation_date
            IS 'Purchase Line Confirmation Date';
            """
        )
