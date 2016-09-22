# -*- coding: utf-8 -*-
# (c) 2016 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Move Import",
    "version": "8.0.1.0.0",
    "category": "Generic Modules",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "contributors": [
        "Daniel Campos <danielcampos@avanzosc.es>",
    ],
    "website": "http://www.avanzosc.es",
    "depends": [
        "account", "stock",
    ],
    "data": [
        "wizard/import_account_move_view.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
}
