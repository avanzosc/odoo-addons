# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Template Lineal",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Inventory",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_lineal_views.xml",
        "views/product_template_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
