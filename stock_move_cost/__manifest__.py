# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Cost",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "depends": [
        "stock_lot_purchase_info",
    ],
    "data": [
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_cost_in_move_lines",
}
