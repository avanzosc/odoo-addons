# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Inventory Transfer Wizard",
    "version": "12.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "stock",
    ],
    "data": [
        "security/stock_inventory_transfer_security.xml",
        "security/ir.model.access.csv",
        "views/stock_inventory_transfer_views.xml",
        "views/stock_inventory_transfer_line_views.xml",
    ],
    "installable": True,
}
