# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Move Line Package Group",
    "version": "14.0.1.0.0",
    "category": "Stock",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "stock_picking_batch",
    ],
    "data": [
        "security/stock_move_line_package_group.xml",
        "views/stock_move_line_view.xml",
    ],
    "installable": True,
}
