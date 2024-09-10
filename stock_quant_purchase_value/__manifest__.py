# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Quant Purchase Value",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_account",
        "stock_production_lot_purchase_cost",
    ],
    "data": [
        "views/stock_quant_views.xml",
    ],
    "installable": True,
}
