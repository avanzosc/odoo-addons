# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Inventory Import Cost",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_inventory_import_wizard",
        "stock_move_line_cost",
    ],
    "data": [
        "views/stock_inventory_import_view.xml",
        "views/stock_inventory_import_line_view.xml",
        "views/stock_inventory_line_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
