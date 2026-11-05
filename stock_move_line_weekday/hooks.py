# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)

_COLUMNS = {
    "weekday": "varchar",
    "year_week": "int4",
    "month": "varchar",
    "year": "int4",
    "warehouse_id": "int4",
    "min_qty": "float8",
}


def pre_init_hook(cr):
    if all(column_exists(cr, "stock_move_line", c) for c in _COLUMNS):
        return
    for col, col_type in _COLUMNS.items():
        if not column_exists(cr, "stock_move_line", col):
            create_column(cr, "stock_move_line", col, col_type)
    _populate_all(cr)


def _populate_all(cr):
    cr.execute(
        """
        WITH base AS (
            SELECT
                sml.id AS line_id,
                sml.product_id,
                sml.location_id,
                COALESCE(sp.date_done, sml.date)::date AS ref_date,
                CAST(EXTRACT(ISODOW FROM COALESCE(sp.date_done, sml.date))
                    AS TEXT) AS weekday_val,
                CAST(EXTRACT(WEEK FROM COALESCE(sp.date_done, sml.date))
                    AS INTEGER) AS year_week_val,
                CAST(EXTRACT(MONTH FROM COALESCE(sp.date_done, sml.date))
                    AS TEXT) AS month_val,
                CAST(EXTRACT(YEAR FROM COALESCE(sp.date_done, sml.date))
                    AS INTEGER) AS year_val,
                spt.warehouse_id AS warehouse_id_val
            FROM stock_move_line sml
            LEFT JOIN stock_picking sp ON sp.id = sml.picking_id
            LEFT JOIN stock_picking_type spt ON spt.id = sp.picking_type_id
        ),
        all_ops AS (
            SELECT
                b.line_id,
                op.id              AS op_id,
                op.product_min_qty,
                ROW_NUMBER() OVER (PARTITION BY b.line_id ORDER BY op.id) AS rn
            FROM base b
            JOIN stock_warehouse_orderpoint op
                ON  op.product_id  = b.product_id
                AND op.location_id = b.location_id
                AND (b.warehouse_id_val IS NULL OR op.warehouse_id = b.warehouse_id_val)
        ),
        first_op AS (
            SELECT line_id, product_min_qty
            FROM all_ops
            WHERE rn = 1
        ),
        specific_rule AS (
            SELECT DISTINCT ON (ao.line_id)
                   ao.line_id,
                   wd.quantity
            FROM all_ops ao
            JOIN base b ON b.line_id = ao.line_id
            JOIN stock_warehouse_orderpoint_weekday wd
                ON  wd.orderpoint_id = ao.op_id
                AND wd.active        = true
                AND wd.type_update   = 'specific'
                AND wd.specific_day  = b.ref_date
                AND wd.quantity IS NOT NULL
                AND wd.quantity != 0
            ORDER BY ao.line_id, wd.sequence
        ),
        weekday_rule AS (
            SELECT DISTINCT ON (ao.line_id)
                   ao.line_id,
                   wd.quantity
            FROM all_ops ao
            JOIN base b ON b.line_id = ao.line_id
            JOIN stock_warehouse_orderpoint_weekday wd
                ON  wd.orderpoint_id = ao.op_id
                AND wd.active        = true
                AND wd.type_update   = 'weekday'
                AND wd.weekday       = b.weekday_val
                AND wd.quantity IS NOT NULL
                AND wd.quantity != 0
            ORDER BY ao.line_id, wd.sequence
        )
        UPDATE stock_move_line sml
        SET
            weekday      = b.weekday_val,
            year_week    = b.year_week_val,
            month        = b.month_val,
            year         = b.year_val,
            warehouse_id = b.warehouse_id_val,
            min_qty      = COALESCE(sr.quantity, wr.quantity, fo.product_min_qty, 0.0)
        FROM base b
        LEFT JOIN first_op      fo ON fo.line_id = b.line_id
        LEFT JOIN specific_rule sr ON sr.line_id = b.line_id
        LEFT JOIN weekday_rule  wr ON wr.line_id = b.line_id
        WHERE sml.id = b.line_id
        """
    )
    _logger.info(
        "stock_move_line_weekday: %d move lines populated",
        cr.rowcount,
    )
