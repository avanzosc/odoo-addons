# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Production Lot Repair Order Shortcut",
    'version': '14.0.1.0.0',
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "repair"
    ],
    "data": [
        "views/stock_production_lot_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
