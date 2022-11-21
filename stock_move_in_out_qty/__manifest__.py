# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move In Out Qty",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
        "stock_move_line_cost"
    ],
    "data": [
        "views/stock_move_line_view.xml",
        "views/stock_move_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
