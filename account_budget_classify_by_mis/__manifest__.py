# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Budget Classify By Mis",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account_budget_oca", "mis_builder"],
    "data": [
        "views/crossovered_budget_views.xml",
        "views/crossovered_budget_lines_views.xml",
    ],
    "installable": True,
}
