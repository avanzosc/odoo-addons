# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Cost",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "depends": [
        "stock_lot_purchase_info",
        "purchase_last_price_info",
    ],
    "data": [
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "_pre_init_stock_move_cost",
    "post_init_hook": "_post_init_stock_move_cost",
}
