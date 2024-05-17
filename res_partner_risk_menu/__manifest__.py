# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Res Partner Risk Menu",
    "version": "14.0.1.0.0",
    "category": "Contacts",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts",
        "account",
        "account_financial_risk",
        "sale_financial_risk",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
