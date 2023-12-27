# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Cleaning Database Operations",
    'version': '14.0.1.0.0',
    "category": "Analytic",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "sale",
        "purchase",
        "account",
        "analytic",
        "mrp",
        "purchase_order_shipping_method"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/cleaning_database_view.xml",
    ],
    'installable': True,
}
