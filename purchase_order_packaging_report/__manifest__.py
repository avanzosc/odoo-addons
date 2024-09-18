# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Packaging Report",
    "version": "14.0.1.0.0",
    "category": "Purchase",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
        "purchase_order_line_qty_by_packaging",
    ],
    "data": [
        "report/purchase_order_report.xml",
    ],
    "installable": True,
}
