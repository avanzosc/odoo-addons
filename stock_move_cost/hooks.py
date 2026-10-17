import logging

from odoo import SUPERUSER_ID, api
from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def install_stock_move_line__price_unit_cost(cr):
    _logger.info("stock_move_cost: Setting price_unit_cost for move lines")
    cr.execute(
        """
        UPDATE stock_move_line ml
        SET price_unit_cost = (SELECT purchase_price_unit
                               FROM   stock_production_lot l
                               WHERE l.id = ml.lot_id)
        WHERE ml.lot_id IS NOT NULL;
        """
    )
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [("standard_price", ">", 0)]
    products = env["product.product"].search(cond)
    for product in products:
        cr.execute(
            """
            UPDATE stock_move_line ml
            SET price_unit_cost = %s
            WHERE ml.lot_id IS NULL
              AND ml.product_id IS NOT NULL
              AND ml.product_id = %s;
            """,
            (
                product.standard_price,
                product.id,
            ),
        )


def install_stock_move_line__cost(cr):
    _logger.info("stock_move_cost: Calculating cost for move lines")
    cr.execute(
        """
        UPDATE stock_move_line ml
        SET cost = ml.price_unit_cost * ml.qty_done
        WHERE ml.price_unit_cost > 0
          AND ml.qty_done > 0;
        """
    )


def install_stock_move__cost(cr):
    _logger.info("stock_move_cost: Calculating cost for stock moves")
    cr.execute(
        """
        UPDATE stock_move sm
        SET cost = sub.total_cost
        FROM (
            SELECT move_id, SUM(cost) as total_cost
            FROM stock_move_line as sm
            WHERE sm.price_unit_cost > 0
              AND sm.qty_done > 0
            GROUP BY move_id
        ) sub
        WHERE sm.id = sub.move_id;
        """
    )


def install_stock_move__price_unit_cost(cr):
    _logger.info("stock_move_cost: Calculating price_unit_cost for stock moves")
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [("cost", ">", 0)]
    moves = env["stock.move"].search(cond)
    for move in moves.filtered(lambda x: x.quantity_done > 0):
        cr.execute(
            """
            UPDATE stock_move
            SET price_unit_cost = %s / %s
            WHERE id = %s;
            """,
            (move.cost, move.quantity_done, move.id),
        )


def _pre_init_stock_move_cost(cr):
    _logger.info("stock_move_cost: Starting pre-init hook")

    if not column_exists(cr, "stock_move_line", "price_unit_cost"):
        create_column(cr, "stock_move_line", "price_unit_cost", "numeric")
    if not column_exists(cr, "stock_move_line", "cost"):
        create_column(cr, "stock_move_line", "cost", "numeric")
    if not column_exists(cr, "stock_move", "price_unit_cost"):
        create_column(cr, "stock_move", "price_unit_cost", "numeric")
    if not column_exists(cr, "stock_move", "cost"):
        create_column(cr, "stock_move", "cost", "numeric")

    _logger.info("stock_move_cost: Pre-init hook completed")


def _post_init_stock_move_cost(cr, registry):
    _logger.info("stock_move_cost: Starting post-init hook")

    install_stock_move_line__price_unit_cost(cr)
    install_stock_move_line__cost(cr)
    install_stock_move__cost(cr)
    install_stock_move__price_unit_cost(cr)

    _logger.info("stock_move_cost: Post-init hook completed")
