# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom Incubator",
    'version': '14.0.2.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock_warehouse_farm",
        "stock_picking_batch_mother",
        "stock_picking_batch_farmer"
    ],
    "data": [
        "views/stock_move_line_view.xml",
        "views/stock_warehouse_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_picking_type_view.xml",
        "views/stock_picking_batch_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
