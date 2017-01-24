# -*- coding: utf-8 -*-
# © 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Print Label",
    "version": "8.0.1.0.0",
    "category": "Warehouse management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "product_expiry_ext",
        "mrp",
    ],
    "data": [
        "data/report_paperformat.xml",
        "wizard/stock_print_label_view.xml",
        "views/mrp_production_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_quant_label_report.xml",
        "views/report_view.xml",
        "views/stock_quant_view.xml",
        "views/product_ul_view.xml"
    ],
    "installable": True,
}
