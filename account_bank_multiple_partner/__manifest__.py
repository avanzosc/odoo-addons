# Copyright 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Bank Multiple Partner",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "summary": """Account Bank Multiple Partner""",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
    ],
    "data": [
        "views/partner_bank_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
