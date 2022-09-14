# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Production Lot Origin Global Gap",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_move_line_views.xml",
        "views/stock_production_lot_views.xml",
    ],
    "installable": True,
}
