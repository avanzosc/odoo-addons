# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Agreement Sale Order Creation",
    "version": "14.0.1.0.0",
    "category": "Contract",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "agreement",
        "agreement_account",
        "agreement_sale",
        "sale_order_type",
        "sale_stock",
    ],
    "excludes": [
        "agreement_stock",
    ],
    "data": [
        "views/agreement_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
