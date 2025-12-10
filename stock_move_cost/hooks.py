def _post_install_put_cost_in_move_lines(env):
    cr = env.cr
    cond = []
    move_lines = env["stock.move.line"].search(cond)
    for move_line in move_lines:
        if move_line.lot_id:
            move_line.update(
                {
                    "price_unit_cost": move_line.lot_id.purchase_price,
                    "cost": move_line.lot_id.purchase_price * move_line.quantity,
                }
            )
        else:
            if move_line.product_id.last_purchase_price:
                price_unit = move_line.product_id.last_purchase_price
            else:
                price_unit = move_line.product_id.standard_price
            cost = price_unit * move_line.quantity
            move_line.update({"price_unit_cost": price_unit, "cost": cost})

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
