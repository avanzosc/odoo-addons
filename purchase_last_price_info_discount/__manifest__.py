# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Last Price Info Discount",
    "version": "18.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "category": "Purchase Management",
    "depends": ["purchase", "purchase_last_price_info"],
    "data": [
        "views/product_template_views.xml",
        "views/product_product_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
