# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Product Catalog",
    "version": "18.0.1.1.0",
    "summary": "Website integration for product catalogs",
    "category": "Website",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": [
        "sale_product_catalog",
        "website",
        "website_sale",
    ],
    "data": [
        "views/product_catalog_views.xml",
        "templates/catalog_detail.xml",
        "templates/catalogs.xml",
        "templates/shop.xml",
        "templates/product.xml",
        "data/website_menu.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_product_catalog/static/src/css/catalog.css",
            "website_sale_product_catalog/static/src/js/catalog_filters.esm.js",
        ],
    },
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
