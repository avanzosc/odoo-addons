# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product's Costs Import Wizard",
    "version": "12.0.2.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_import_wizard",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/product_cost_import_wizard_security.xml",
        "views/product_cost_import_views.xml",
        "views/product_cost_import_line_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
