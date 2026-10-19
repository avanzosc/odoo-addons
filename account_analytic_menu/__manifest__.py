# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Analytic Menu",
    "summary": (
        "Adds a non-technical 'Analytic' menu with Analytic Accounts "
        "under the main Accounting menu"
    ),
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account", "analytic"],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Accounting/Accounting",
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_menu.xml",
    ],
    "installable": True,
    "application": False,
}
