# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Packaging Import Wizard",
    "version": "14.0.2.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "product",
        "delivery",
        "product_packaging_dimension",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_packaging_import_view.xml",
        "views/product_packaging_import_line_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
