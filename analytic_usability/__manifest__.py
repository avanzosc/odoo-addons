# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Analytic Usability",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Tools",
    "depends": [
        "analytic",
        "account",
    ],
    "data": [
        "security/analytic_usability_groups.xml",
        "views/account_analytic_account_view.xml",
        "views/account_analytic_line_view.xml",
        "views/res_config_view.xml",
    ],
    "installable": True,
}
