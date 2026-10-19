# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Reconciliation Manual Date Due",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account", "account_reconcile_oca"],
    "data": [
        "views/account_bank_statement_line_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
