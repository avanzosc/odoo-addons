# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    stock_move_create_new_fields(cr)
    store_field_stored_purchase_price_unit(cr)


def stock_move_create_new_fields(cr):
    cr.execute("""
        ALTER TABLE stock_move
        ADD purchase_price_unit float
    """)


def store_field_stored_purchase_price_unit(cr):
    cr.execute("""
        UPDATE stock_move
        SET   purchase_price_unit = (SELECT purchase_order_line.price_unit
                                     FROM   purchase_order_line
                                     WHERE  stock_move.purchase_line_id =
                                            purchase_order_line.id)
        WHERE purchase_line_id is not null
    """)
