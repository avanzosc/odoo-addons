# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contacts Import Wizard - Custom Saca extension",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts_import_wizard",
        "custom_saca",
    ],
    "data": [
        "views/res_partner_import_views.xml",
        "views/res_partner_import_line_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
