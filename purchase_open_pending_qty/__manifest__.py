# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Open Pending Qty",
    "version": "18.0.1.0.0",
    "category": "Inventory/Purchase",
    "summary": "Add pending qty columns and line copy action on purchases",
    "depends": ["purchase_open_qty"],
    "data": [
        "views/purchase_order_line_view.xml",
        "views/purchase_order_view.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
}
