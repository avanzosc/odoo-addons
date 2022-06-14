# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Batch Farmer",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock_warehouse_farm",
        "stock_picking_batch_mother",
        "stock_picking_batch_breeding",
        
    ],
    "data": [
        "views/stock_picking_batch_view.xml",
        "views/stock_picking_view.xml"
    ],
    "installable": True,
}
