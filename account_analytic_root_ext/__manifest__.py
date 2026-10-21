# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Analytic Root Ext",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Account",
    "depends": [
        "analytic_usability",
        "account_analytic_root",
    ],
    "data": [
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
