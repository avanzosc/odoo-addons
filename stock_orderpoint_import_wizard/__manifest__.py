# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Minimum Inventory Rule import wizard",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/stock_orderpoint_wizard_security.xml",
        "views/stock_warehouse_orderpoint_import_views.xml",
        "views/stock_warehouse_orderpoint_import_line_views.xml",
    ],
    "installable": True,
}
