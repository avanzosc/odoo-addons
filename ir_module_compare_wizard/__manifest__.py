# Copyright 2024 Unai Beristain, Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Module Comparing Wizard",
    "version": "16.0.1.1.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base",
        "base_import_wizard",
    ],
    "data": [
        "views/ir_module_import_views.xml",
        "views/ir_module_import_line_views.xml",
        "security/ir.model.access.csv",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
