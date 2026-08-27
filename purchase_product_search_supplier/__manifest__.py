# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Product Search Supplier",
    "summary": "On POs, search product first by supplier code/name (supplierinfo)",
    "version": "16.0.1.0.0",
    "category": "Purchase",
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
