# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Catalog Web",
    "version": "18.0.1.0.0",
    "summary": "Product catalog management for web",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "base",
        "product",
        "stock",
        "sale",
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/product_catalog_web_rules.xml",
        "wizard/import_catalog_views.xml",
        "views/product_catalog_web_views.xml",
        "views/menus.xml",
        "templates/product_catalog.xml",
    ],
    "installable": True,
    "application": False,
}
