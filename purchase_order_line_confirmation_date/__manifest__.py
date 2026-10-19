# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Line Confirmation Date",
    "version": "16.0.1.0.0",
    "category": "Purchases",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_stock",
    ],
    "excludes": [],
    "data": [
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
