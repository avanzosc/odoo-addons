# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Lot Last Move Locations",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["product", "stock"],
    "data": [
        "views/stock_lot_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_last_move_locations_in_lots",
}
