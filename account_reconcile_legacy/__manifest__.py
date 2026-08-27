# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Reconcile Legacy",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account_accountant",
    ],
    "data": [
        "data/account_reconcile_legacy.xml",
        "views/account_move_line_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "account_reconcile_legacy/static/src/js/account_reconcile_legacy_view.esm.js",
            "account_reconcile_legacy/static/src/js/account_manual_reconcile_legacy_view.esm.js",
            "account_reconcile_legacy/static/src/xml/account_bank_reconcile_legacy_view.xml",
            "account_reconcile_legacy/static/src/xml/account_manual_reconcile_legacy_view.xml",
            "account_reconcile_legacy/static/src/scss/account_reconcile_legacy_view.scss",
            "account_reconcile_legacy/static/src/scss/account_manual_reconcile_legacy_view.scss",
        ],
    },
    "installable": True,
}
