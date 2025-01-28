# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Packaging Report",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Purchase",
    "license": "AGPL-3",
    "depends": ["purchase", "purchase_order_line_qty_by_packaging"],
    "data": [
        "report/report_purchaseorder.xml",
        "report/report_purchasequotation.xml",
    ],
    "installable": True,
}
