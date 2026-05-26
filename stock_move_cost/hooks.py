def _post_install_put_cost_in_move_lines(env):
    cr = env.cr

    cr.execute(
        """
        UPDATE stock_move_line ml
        SET price_unit_cost = (
            SELECT purchase_price FROM stock_lot l WHERE l.id = ml.lot_id)
        WHERE lot_id IS NOT NULL;
        """
    )

    move_lines = env["stock.move.line"].search([("lot_id", "=", False)])
    for move_line in move_lines:
        if move_line.product_id.last_purchase_price:
            price_unit = move_line.product_id.last_purchase_price
        else:
            price_unit = move_line.product_id.standard_price
        cost = price_unit * move_line.quantity
        move_line.update({"price_unit_cost": price_unit, "cost": cost})

    cr.execute(
        """
        UPDATE stock_move_line
        SET cost = price_unit_cost * quantity
        WHERE price_unit_cost > 0
          AND quantity > 0;
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
        SET price_unit_cost = cost / quantity
        where cost > 0
          and quantity > 0;
        """
    )
