# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Return",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Sales",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_order_confirm_usability",
        "purchase_open_qty",
        "stock_move_line_force_done",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
