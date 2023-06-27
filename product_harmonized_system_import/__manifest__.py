# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Harmonized System Import",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product_import_wizard",
        "product_harmonized_system",
    ],
    "data": [
        "views/product_import_view.xml",
        "views/product_import_line_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
