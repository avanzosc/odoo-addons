# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Pickings Import Wizard",
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
        "stock_picking_batch_breeding",
        "stock_picking_date_done",
        "stock_warehouse_farm",
        "purchase_order_shipping_method",
        "stock_move_line_cost"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/pickings_import_wizard_security.xml",
        "views/stock_picking_import_views.xml",
        "views/stock_picking_import_line_views.xml",
        "views/delivery_carrier_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
