# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product State Values",
    "version": "18.0.1.0.0",
    "category": "Product",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "product_state",
    ],
    "data": [
        "data/product_state_values.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
