# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Move Line Type",
    "summary": "Adds a computed type field to stock move lines based on location usage.",
    "version": "14.0.1.0.0",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": ["stock"],
    "data": [
        "views/stock_move_line_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
