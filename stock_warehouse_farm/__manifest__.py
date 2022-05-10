# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Warehouse Farm Data",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
        "base_geolocalize",
        "contacts",
        "stock_location_warehouse",
        "stock_picking_batch"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/category_type.xml",
        "views/category_type_views.xml",
        "views/product_category_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_warehouse_view.xml",
        "views/res_partner_view.xml",
        "views/picking_batch_stage_views.xml",
        "views/stock_picking_batch_views.xml",
    ],
    "installable": True,
}
