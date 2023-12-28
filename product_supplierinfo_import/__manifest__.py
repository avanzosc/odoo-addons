# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Supplierinfo Import",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "stock",
        "purchase",
        "purchase_discount",
        "product_trim_name",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/product_supplierinfo_import_security.xml",
        "views/product_supplierinfo_import_line_views.xml",
        "views/product_supplierinfo_import_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
