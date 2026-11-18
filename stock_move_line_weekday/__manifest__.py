# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Move Line Weekday",
    "summary": "Adds weekday, week, month, year, warehouse and min. qty. to stock move lines.",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "depends": [
        "stock_move_line_type",
        "stock_orderpoint_weekday",
    ],
    "data": [
        "views/stock_move_line_view.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
