# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)
{
    "name": "Stock Move With Partner",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Add partner information to stock moves and move lines",
    "description": """
    This module extends the stock functionality by adding partner 
    (customer/supplier) information to both stock movements and their lines.""",
    "depends": [
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "data": [
        "views/stock_move_views.xml",
        "views/stock_move_line_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}