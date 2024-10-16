# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Import With Packaging",
    "version": "14.0.2.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product_import_wizard",
        "product_packaging_import_wizard",
    ],
    "data": [
        "views/product_import_view.xml",
        "views/product_import_line_view.xml",
        "views/product_packaging_import_view.xml",
    ],
    "installable": True,
}
