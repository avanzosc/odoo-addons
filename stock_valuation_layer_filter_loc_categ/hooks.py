# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def load_data_into_stock_valuation_layer(cr, registry):
    cr.execute(
        "UPDATE stock_valuation_layer "
        "set product_categ_id = (select product_template.categ_id "
        "from product_product, product_template "
        "where product_product.id = stock_valuation_layer.product_id "
        "and product_template.id = product_product.product_tmpl_id) "
        "where product_id is not null"
    )

    cr.execute(
        "update stock_valuation_layer "
        "set not_show_category_in_inventory_reports = "
        "(select product_category.not_show_in_inventory_reports "
        "from product_category "
        "where product_category.id = stock_valuation_layer.product_categ_id) "
        "where product_categ_id is not null"
    )

    cr.execute(
        "update stock_valuation_layer "
        "set location_id = (select stock_move.location_id "
        "from stock_move "
        "where stock_move.id = stock_valuation_layer.stock_move_id) "
        "where stock_move_id is not null"
    )

    cr.execute(
        "update stock_valuation_layer "
        "set location_dest_id = (select stock_move.location_dest_id "
        "from stock_move "
        "where stock_move.id = stock_valuation_layer.stock_move_id) "
        "where stock_move_id is not null"
    )

    cr.execute(
        "update stock_valuation_layer "
        "set not_show_category_in_inventory_reports = False,"
        "not_show_location_in_inventory_reports = False "
        "where stock_move_id is null"
    )

    cr.execute(
        "update stock_valuation_layer "
        "set not_show_category_in_inventory_reports = "
        "(select stock_move.not_show_category_in_inventory_reports "
        "from stock_move "
        "where stock_move.id = stock_valuation_layer.stock_move_id) "
        "where stock_move_id is not null"
    )

    cr.execute(
        "update stock_valuation_layer "
        "set not_show_location_in_inventory_reports = "
        "(select stock_move.not_show_location_in_inventory_reports "
        "from stock_move "
        "where stock_move.id = stock_valuation_layer.stock_move_id) "
        "where stock_move_id is not null"
    )
