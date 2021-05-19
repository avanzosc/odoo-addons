# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State Tag",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Customized module",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "data/product_state_tag_data.xml",
        "security/ir.model.access.csv",
        "views/product_state_views.xml",
        "views/product_tag_views.xml",
        "views/product_product_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
