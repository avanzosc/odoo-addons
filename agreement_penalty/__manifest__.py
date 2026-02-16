# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Agreement Penalty Type",
    "version": "14.0.1.0.0",
    "category": "Contract",
    "summary": "Per-agreement penalty types and settings",
    "depends": [
        "agreement",
        "account_penalty",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/agreement_view.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
}
