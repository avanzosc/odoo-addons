from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_cost_in_move_lines(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [("standard_price", ">", 0)]
    products = env["product.product"].search(cond)
    for product in products:
        cr.execute(
            """
            UPDATE stock_move_line
            SET price_unit_cost = %s
            WHERE product_id = %s;
            """,
            (
                product.standard_price,
                product.id,
            ),
        )
    cr.execute(
        """
        UPDATE stock_move_line
           SET price_unit_cost = (
                   SELECT stock_production_lot.purchase_price_unit
                     FROM stock_production_lot
                    WHERE stock_production_lot.id = stock_move_line.lot_id)
        WHERE lot_id IS NOT null
        """
    )

    cr.execute(
        """
        UPDATE stock_move_line
           SET cost = stock_move_line.price_unit_cost * stock_move_line.qty_done;
        """
    )

    cr.execute(
        """
        UPDATE stock_move
           SET cost = (
                SELECT sum(stock_move_line.cost)
                  FROM stock_move_line
                 WHERE stock_move_line.move_id = stock_move.id);
        """
    )

    cr.execute(
        """
        UPDATE stock_move
           SET price_unit_cost = stock_move.cost / (
                   SELECT sum(stock_move_line.qty_done)
                     FROM stock_move_line
                    WHERE stock_move_line.move_id = stock_move.id)
         WHERE cost > 0;
        """
    )
