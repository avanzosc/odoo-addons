# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Stock Supplier",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory/Purchase",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "purchase_stock",
    ],
    "data": [
        "views/stock_warehouse_orderpoint_views.xml",
    ],
    'installable': True,
}
