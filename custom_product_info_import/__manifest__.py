# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Product Info Import",
    "version": "12.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "custom_product_info",
        "product_import_wizard",
    ],
    "data": [
        "views/product_import_line_view.xml",
        "views/product_import_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
