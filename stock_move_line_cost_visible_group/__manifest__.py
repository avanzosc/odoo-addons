# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Line Cost Visible Group",
    "version": "18.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_move_line_cost",
    ],
    "data": [
        "data/stock_move_line_cost_group.xml",
        "views/stock_move_line_view.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
