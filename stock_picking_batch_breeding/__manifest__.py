# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Breeding",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "depends": [
        "stock_picking_batch",
        "stock_production_lot_mother",
        "stock_location_warehouse"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/picking_batch_stage.xml",
        "data/category_type.xml",
        "views/category_type_views.xml",
        "views/product_category_views.xml",
        "views/stock_warehouse_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/stock_picking_views.xml",
        "views/picking_batch_stage_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
