# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Package Usability",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "delivery_package_number",
        "stock_quant_package_volume"
    ],
    "data": [
        "views/stock_quant_package_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_line_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
