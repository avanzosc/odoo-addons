# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom P",
    "version": "14.0.1.0.0",
    "category": "Custom",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale_stock",
        "sale_order_return",
        "sale_order_line_price_history",
        "sale_order_lot_selection",
        "sale_order_line_commitment_date",
        "account",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "wizards/sale_order_line_price_history_view.xml",
    ],
    "installable": True,
}
