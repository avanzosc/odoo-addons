# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Picking Label Print",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "category": "Warehouse Management",
    "website": "http://www.avanzosc.es",
    "contributors": ["Ainara Galdona <ainaragaldona@avanzosc.es>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>"],
    "depends": ["stock"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/report_paperformat.xml",
        "views/product_ul_view.xml",
        "views/stock_label_report_data_view.xml",
        "views/stock_picking_view.xml",
        "wizard/stock_transfer_details_view.xml",
        "views/stock_label_report.xml",
        "views/report_view.xml"
        ],
    "installable": True
}
