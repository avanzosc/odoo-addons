# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchases for Fleet Vehicle",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Fleet",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
        "fleet",
        "project_vehicle",
    ],
    "data": [
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "_pre_init_purchase_fleet",
}
