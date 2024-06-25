# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Res Partner Rappel",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Contacts",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contacts",
        "account",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_partner_rappel_security.xml",
        "views/res_partner_view.xml",
        "views/account_move_line_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
