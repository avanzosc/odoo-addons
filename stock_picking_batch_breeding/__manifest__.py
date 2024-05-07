# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Breeding",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "depends": [
        "stock_warehouse_farm",
        "stock_picking_batch_mother",
        "stock_move_line_cost",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/picking_batch_stage.xml",
        "data/in_out_decimal_precision.xml",
        "data/breeding_name_seq.xml",
        "views/stock_picking_batch_views.xml",
        "views/breeding_feed_views.xml",
        "views/stock_picking_views.xml",
        "views/growth_rate_views.xml",
        "views/lineage_views.xml",
        "views/estimate_weight_views.xml",
        "views/stock_move_line_views.xml",
        "views/product_template_views.xml",
        "views/res_partner_view.xml",
        "views/mother_lineage_relation_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
