# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact Supplier Payment Term Access",
    "version": "18.0.1.0.0",
    "category": "Contacts",
    "summary": "Access to supplier payment terms without accounting permissions",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account"],
    "data": [
        "security/res_groups.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "application": False,
}
