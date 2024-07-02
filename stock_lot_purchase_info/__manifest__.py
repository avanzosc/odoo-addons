# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Lot Purchase Info",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
        "stock",
    ],
    "data": [
        "views/stock_lots_views.xml",
        "views/stock_move_line_views.xml",
    ],
    "installable": True,
}
