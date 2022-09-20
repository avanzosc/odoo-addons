# Copyright 2022 Patxi lersundi
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Final",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Warehouse",
    "license": "AGPL-3",
    "version": "12.0.2.0.0",
    "depends": [
        "stock",
        "product",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_final_views.xml",
        "views/product_location_exploded_views.xml",
        "views/product_product_views.xml",
        "views/product_final_import_views.xml",
        "views/product_final_import_line_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
