# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Pickings Batch Import",
    "version": "14.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "base_import_wizard",
        "stock_picking_batch",
        "stock_warehouse_farm",
        "stock_picking_batch_mother",
        "stock_picking_batch_breeding",
        "stock_picking_date_done",
        "stock_warehouse_farm",
        "stock_move_line_cost",
        "custom_pickings_import_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/picking_batch_import_security.xml",
        "views/stock_picking_batch_import_view.xml",
        "views/stock_picking_batch_import_line_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
