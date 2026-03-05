# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Move Plastic Weight",
    "summary": "Shows total weight of recycled and non-recycled plastic on invoices",
    "version": "16.0.1.0.0",
    "category": "Accounting/Localizations",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
        "l10n_es_aeat_mod592",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
}
