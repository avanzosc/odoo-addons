# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Move Personal Name",
    "version": "18.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_move_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "account_move_personal_name/static/src/scss/personal_name.scss",
        ],
    },
    "installable": True,
    "post_init_hook": "post_init_hook",
}
