# Copyright 2025 Lucía Echeverría- AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Move Line Display Fields",
    "version": "14.0.1.0.0",
    "category": "Inventory",
    "summary": "Adds additional columns in the detailed operations views of delivery orders",
    "author": "AvanzOSC",
    "depends": [
        "stock_move_qty_by_packaging",
        "stock_move_line_product_lot_reader",
        "custom_mrp_line_cost",
    ],
    "data": [
        "views/stock_move_line_view.xml",
    ],
    "website": "https://github.com/avanzosc/odoo-addons",
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}
