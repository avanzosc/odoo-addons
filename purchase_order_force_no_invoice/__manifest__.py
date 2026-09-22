# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Force No Invoice",
    "summary": 'Force a purchase order\'s billing status to "Nothing to Bill"',
    "version": "18.0.1.0.0",
    "category": "Purchases",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
