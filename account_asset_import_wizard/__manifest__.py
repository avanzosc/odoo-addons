# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Asset Import Wizard",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account_asset_management",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/account_asset_line_import_security.xml",
        "views/account_asset_line_import_line_view.xml",
        "views/account_asset_line_import_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
