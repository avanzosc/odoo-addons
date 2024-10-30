# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Base Import Wizard",
    "version": "18.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/base_import_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
