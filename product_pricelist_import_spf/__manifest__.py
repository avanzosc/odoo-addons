# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SPF Pricelist Import",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "base",
        "product",
        "sale",
        "sale_product_catalog",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_pricelist_views.xml",
        "views/product_pricelist_market_views.xml",
        "views/product_pricelist_item_import_views.xml",
    ],
    "installable": True,
    "application": False,
}
