# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Mother",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "depends": [
        "stock_warehouse_farm",
        "stock_picking_batch",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/picking_batch_stage.xml",
        "views/stock_picking_batch_views.xml",
        "views/lineage_views.xml",
        "views/birth_rate_views.xml",
        "views/laying_rate_views.xml",
        "views/product_template_views.xml",
        "views/stock_production_lot_views.xml",
        "views/stock_picking_view.xml",
        "views/cancellation_line_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
