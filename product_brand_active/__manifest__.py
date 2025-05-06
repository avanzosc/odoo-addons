# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Brand Active",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product_brand",
    ],
    "data": [
        "views/product_brand_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_active_product_brand",
}
