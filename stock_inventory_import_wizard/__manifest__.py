# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Inventory Import Wizard",
    "version": "12.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_inventory_import_line_views.xml",
        "views/stock_inventory_import_views.xml",
        "views/stock_inventory_line_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
