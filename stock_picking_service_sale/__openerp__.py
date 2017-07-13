# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Picking Service Sale",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "category": "Warehouse Management",
    "website": "http://www.avanzosc.es",
    "contributors": ["Ainara Galdona <ainaragaldona@avanzosc.es>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>"],
    "depends": ["sale_stock",
                "stock_picking_taxes"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_report.xml",
        "views/stock_picking_view.xml"
        ],
    "installable": True
}
