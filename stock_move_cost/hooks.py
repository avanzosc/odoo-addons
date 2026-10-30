import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def install_stock_move_line__price_unit_cost(env):
    _logger.info("stock_move_cost: Setting price_unit_cost for move lines")
    env.cr.execute(
        """
        UPDATE stock_move_line ml
        SET price_unit_cost = CASE
            WHEN ml.lot_id IS NOT NULL THEN
                (SELECT purchase_price FROM stock_lot l WHERE l.id = ml.lot_id)
            ELSE
                COALESCE(
                    NULLIF(
                        (SELECT pol.price_unit
                         FROM purchase_order_line pol
                         JOIN purchase_order po ON po.id = pol.order_id
                         WHERE pol.product_id = ml.product_id
                           AND pol.state IN ('purchase', 'done')
                         ORDER BY po.date_order DESC, pol.id DESC
                         LIMIT 1),
                        0),
                    (SELECT (pp.standard_price ->> ml.company_id::text)::numeric
                     FROM product_product pp
                     WHERE pp.id = ml.product_id),
                    0)
        END
        WHERE ml.lot_id IS NOT NULL
           OR (ml.lot_id IS NULL AND ml.product_id IS NOT NULL);
        """
    )


def install_stock_move_line__cost(env):
    _logger.info("stock_move_cost: Calculating cost for move lines")
    env.cr.execute(
        """
        UPDATE stock_move_line ml
        SET cost = ml.price_unit_cost * ml.quantity
        WHERE ml.price_unit_cost > 0
          AND ml.quantity > 0;
        """
    )


def install_stock_move__cost(env):
    _logger.info("stock_move_cost: Calculating cost for stock moves")
    env.cr.execute(
        """
        UPDATE stock_move sm
        SET cost = sub.total_cost
        FROM (
            SELECT move_id, SUM(cost) as total_cost
            FROM stock_move_line as sm
            WHERE sm.price_unit_cost > 0
              AND sm.quantity > 0
            GROUP BY move_id
        ) sub
        WHERE sm.id = sub.move_id;
        """
    )


def install_stock_move__price_unit_cost(env):
    _logger.info("stock_move_cost: Calculating price_unit_cost for stock moves")
    env.cr.execute(
        """
        UPDATE stock_move sm
        SET price_unit_cost = sm.cost / sm.quantity
        WHERE sm.cost > 0
          AND sm.quantity > 0;
        """
    )


def _pre_init_stock_move_cost(env):
    _logger.info("stock_move_cost: Starting pre-init hook")

    if not column_exists(env.cr, "stock_move_line", "price_unit_cost"):
        create_column(env.cr, "stock_move_line", "price_unit_cost", "numeric")
    if not column_exists(env.cr, "stock_move_line", "cost"):
        create_column(env.cr, "stock_move_line", "cost", "numeric")
    if not column_exists(env.cr, "stock_move", "price_unit_cost"):
        create_column(env.cr, "stock_move", "price_unit_cost", "numeric")
    if not column_exists(env.cr, "stock_move", "cost"):
        create_column(env.cr, "stock_move", "cost", "numeric")

    _logger.info("stock_move_cost: Pre-init hook completed")


def _post_init_stock_move_cost(env):
    _logger.info("stock_move_cost: Starting post-init hook")

    install_stock_move_line__price_unit_cost(env)
    install_stock_move_line__cost(env)
    install_stock_move__cost(env)
    install_stock_move__price_unit_cost(env)

    _logger.info("stock_move_cost: Post-init hook completed")
