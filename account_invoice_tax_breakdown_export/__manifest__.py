# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Invoice export xlsx with Tax Breakdown",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
    ],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "wizards/account_invoice_xlsx_export_views.xml",
    ],
    "installable": True,
}
