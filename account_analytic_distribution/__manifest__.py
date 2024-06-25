# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Analytic Distribution",
    "version": "14.0.1.0.0",
    "category": "Analytic",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
        "analytic",
        "analytic_usability",
        "account_due_list",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/account_analytic_template_security.xml",
        "views/account_move_view.xml",
        "views/account_move_line_view.xml",
        "views/account_account_view.xml",
        "views/account_analytic_template_view.xml",
    ],
    "installable": True,
}
