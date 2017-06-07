# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Label Print",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "category": "Manufacturing",
    "website": "http://www.avanzosc.es",
    "contributors": ["Ainara Galdona <ainaragaldona@avanzosc.es>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>"],
    "depends": ["stock_picking_label_print", "mrp"],
    "data": [
        "views/stock_label_report_data_view.xml",
        "views/mrp_production_view.xml",
        "wizard/mrp_product_produce_view.xml"
        ],
    "installable": True
}
