# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Supplier Pricelist Import Wizard",
    "version": "18.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "product",
    ],
    "excludes": [],
    "data": [
        "security/product_supplierinfo_wizard_security.xml",
        "security/ir.model.access.csv",
        "views/product_supplierinfo_import_views.xml",
        "views/product_supplierinfo_import_line_views.xml",
    ],
    "installable": True,
}
