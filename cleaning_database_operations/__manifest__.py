# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Cleaning Database Operations",
    "version": "16.0.1.0.0",
    "category": "Generic Modules",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "sale",
        "purchase",
        "account",
        "account_payment_order",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/cleaning_database_view.xml",
        "wizards/cleaning_database_warning_wizard_view.xml",
    ],
    "installable": True,
}
