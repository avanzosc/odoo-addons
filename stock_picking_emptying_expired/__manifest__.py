# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Emptying Expired",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "product",
        "product_expiry",
        "stock",
        "product_expiry_no_lot",
        "stock_picking_date_done",
    ],
    "data": [
        "views/stock_picking_type_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
