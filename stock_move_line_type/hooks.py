# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    if column_exists(cr, "stock_move_line", "move_line_type"):
        return
    create_column(cr, "stock_move_line", "move_line_type", "varchar")
    cr.execute(
        """
        UPDATE stock_move_line sml
        SET move_line_type = CASE
            WHEN sl_src.usage != 'internal' AND sl_dst.usage = 'internal'
                THEN 'incoming'
            WHEN sl_src.usage = 'internal' AND sl_dst.usage != 'internal'
                 AND sl_dst.scrap_location = true
                THEN 'expired'
            WHEN sl_src.usage = 'internal' AND sl_dst.usage != 'internal'
                THEN 'outgoing'
            WHEN sl_src.usage = 'internal' AND sl_dst.usage = 'internal'
                THEN 'internal'
            ELSE 'other'
        END
        FROM stock_location sl_src,
             stock_location sl_dst
        WHERE sml.location_id = sl_src.id
          AND sml.location_dest_id = sl_dst.id
        """
    )
    _logger.info(
        "stock_move_line_type: %d move lines populated with move_line_type",
        cr.rowcount,
    )
