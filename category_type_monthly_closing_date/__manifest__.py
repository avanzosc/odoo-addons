# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Category Type Monthly Closing Date",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "stock_picking_date_done",
        "stock_warehouse_farm",
    ],
    "data": [
        "views/category_type_view.xml",
        "views/stock_move_line_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
