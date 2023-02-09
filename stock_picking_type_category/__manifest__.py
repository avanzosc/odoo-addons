# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Category Type",
    "version": "14.0.1.0.0",
    "category": "MRP",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_type_view.xml",
        "views/stock_picking_type_category_view.xml",
    ],
    "installable": True,
}
