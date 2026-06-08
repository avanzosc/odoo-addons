# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Stock Orderpoint Qty",
    "version": "18.0.1.0.0",
    "category": "Stock",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "stock_orderpoint_usability",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "data/server_actions.xml",
    ],
    "installable": True,
}
