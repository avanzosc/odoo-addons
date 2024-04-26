# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact Payment Mode Import",
    "version": "16.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts",
        "base_import_wizard",
        "account",
        "account_payment_mode",
        "account_payment_partner",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/contact_payment_mode_import_security.xml",
        "views/res_partner_import_line_views.xml",
        "views/res_partner_import_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
