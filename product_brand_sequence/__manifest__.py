# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Product Brand Sequence",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "product_brand",
    ],
    "author": "AvanzOSC",
    "category": "Product",
    "website": "http://www.avanzosc.es",
    "data": [
        "views/product_view.xml",
    ],
    "installable": True,
    'post_init_hook': 'post_init_hook',
}
