# Copyright 2024 Unai Beristain, Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Module Comparing Wizard",
    "version": "18.0.1.2.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/odoo_version_data.xml",
        "views/ir_module_import_views.xml",
        "views/ir_module_import_line_views.xml",
        "views/migration_category_views.xml",
        "views/odoo_version_views.xml",
        "views/ir_module_module_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
