# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Cost Visible",
    "version": "14.0.1.0.0",
    "category": "Purchase Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["purchase_last_price_info"],
    "data": [
        "data/product_cost_groups.xml",
        "data/res_groups.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
