# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Pickings Import Wizard",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "product",
        "base_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/pickings_import_wizard_security.xml",
        "views/stock_picking_import_views.xml",
        "views/stock_picking_import_line_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
