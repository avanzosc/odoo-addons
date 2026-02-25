# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Open Pending Qty",
    "version": "18.0.1.0.0",
    "category": "Inventory/Purchase",
    "summary": "Technical wrapper for purchase_open_qty with optional line copy action",
    "depends": ["purchase_open_qty"],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
}
