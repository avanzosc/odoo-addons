# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order List Column Width",
    "summary": "Fix the width of the priority and alternatives columns "
    "in the purchase order lists",
    "version": "18.0.1.0.0",
    "category": "Purchases",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
        "purchase_requisition",
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
