# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Asset Cleaning Database Operations",
    "version": "16.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "cleaning_database_operations",
        "account_asset_management",
    ],
    "data": [
        "views/cleaning_database_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
