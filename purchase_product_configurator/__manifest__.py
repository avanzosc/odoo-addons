# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Product Configurator",
    "version": "18.0.1.0.0",
    "author": "AvanzOSC",
    "category": "Purchases/Purchases",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "sale",
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "purchase_product_configurator/static/src/js/purchase_product_field.esm.js",
            "purchase_product_configurator/static/src/xml/purchase_product_field.xml",
        ],
    },
    "installable": True,
    "application": False,
}
