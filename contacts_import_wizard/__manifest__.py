# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contacts Import Wizard",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "contacts",
        "base_import_wizard",
        "base_address_city",
        "base_location",
        "l10n_es_partner",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/contacts_import_wizard_security.xml",
        "views/res_partner_import_views.xml",
        "views/res_partner_import_line_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
