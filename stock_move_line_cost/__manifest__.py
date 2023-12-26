# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Line Cost",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "sale_stock",
        "purchase_stock",
        "stock_move_line_force_done",
    ],
    "data": [
        "views/stock_move_line_view.xml",
        "views/stock_picking_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
