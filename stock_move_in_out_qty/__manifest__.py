# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Move In Out Qty",
    "version": "18.0.1.0.0",
    "summary": """Adds incoming, outgoing and difference
    quantity fields to stock moves, move lines and lots""",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["stock"],
    "data": [
        "views/stock_lot_view.xml",
        "views/stock_move_line_view.xml",
        "views/stock_move_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
