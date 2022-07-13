# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Import Wizard",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_import_views.xml",
        "views/product_import_line_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
