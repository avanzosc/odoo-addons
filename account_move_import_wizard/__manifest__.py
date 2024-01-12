# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Move Import Wizard",
    "version": "16.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
        "account_move_unbalanced",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/account_move_import_security.xml",
        "views/account_move_import_line_view.xml",
        "views/account_move_import_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
