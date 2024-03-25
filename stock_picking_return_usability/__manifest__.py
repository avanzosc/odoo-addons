# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Return Usability",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["stock", "stock_move_line_force_done"],
    "data": [
        "views/stock_picking_type_view.xml",
        "wizard/stock_return_picking_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
