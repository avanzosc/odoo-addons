# Copyright 2024 Unai Beristain, Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Module Compare Wizard",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
    ],
    "data": [
        "views/ir_module_import_line_views.xml",
        "views/ir_module_import_views.xml",
        "views/ir_module_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
