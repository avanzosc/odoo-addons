# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Report Order",
    "summary": "Ascendent name order for account invoices.",
    "version": "18.0.1.0.0",
    "category": "Invoices & Payments",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "account_invoice_report_order/static/src/js/pivot_invoice_order.esm.js",
        ],
    },
    "installable": True,
    "application": False,
}
