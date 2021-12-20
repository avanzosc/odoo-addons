# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Packaging Volume",
    'version': '14.0.2.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "depends": [
        "stock",
        "delivery",
        "product_packaging_dimension"
    ],
    "data": [
        "views/product_packaging_views.xml",
        "views/stock_move_line_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
