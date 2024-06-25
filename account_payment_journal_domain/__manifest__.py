# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Payment Journal Domain",
    "version": "14.0.1.0.0",
    "category": "Analytic",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_payment_view.xml",
        "views/account_journal_view.xml",
        "wizard/account_payment_registrer_view.xml",
    ],
    "installable": True,
}
