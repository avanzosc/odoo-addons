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
        SET price_unit_cost = (select stock_lot.purchase_price
                               from stock_lot
                               where stock_lot.id = stock_move_line.lot_id)
        WHERE lot_id is not null
        """
    )

    cr.execute(
        """
        UPDATE stock_move_line
        SET cost = price_unit_cost * qty_done;
        """
    )

    cr.execute(
        """
        UPDATE stock_move
        SET cost = (select sum(stock_move_line.cost)
                    from   stock_move_line
                    where  stock_move_line.move_id = stock_move.id);
        """
    )

    cr.execute(
        """
        UPDATE stock_move
        SET price_unit_cost = cost / quantity_done
        where cost > 0
          and quantity_done > 0;
        """
    )
