# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Line Package Dimension",
    'version': '14.0.2.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "depends": [
        "stock",
        "delivery",
        "product_packaging_dimension",
        "stock_picking_package_usability"
    ],
    "data": [
        "views/stock_move_line_views.xml",
        "views/product_packaging_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
