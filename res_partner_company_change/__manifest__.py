# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Res Partner Company Change",
    "version": "12.0.1.0.0",
    "category": "Contacts",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts",
        "purchase",
        "account",
        "delivery",
        "account_payment_partner",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_company_change_line_view.xml",
        "views/res_partner_company_change_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
