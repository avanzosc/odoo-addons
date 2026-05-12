# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Res Partner Historical Risk",
    "version": "14.0.1.0.0",
    "category": "Contacts",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account",
        "res_partner_risk_menu",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_partner_historical_risk_security.xml",
        "views/res_partner_historical_risk_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
