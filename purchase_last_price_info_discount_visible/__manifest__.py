# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Last Price Info Discount Visible",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "category": "Purchase Management",
    "depends": [
        "purchase_last_price_info_discount",
        "product_cost_visible"
    ],
    "data": [
        "views/product_template_views.xml",
        "views/product_product_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
