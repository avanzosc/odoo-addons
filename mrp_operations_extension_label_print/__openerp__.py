# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Operations Extension Label Print",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "category": "Manufacturing",
    "website": "http://www.avanzosc.es",
    "contributors": ["Ainara Galdona <ainaragaldona@avanzosc.es>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>"],
    "depends": ["mrp_label_print", "mrp_operations_extension"],
    "data": [
        "wizard/mrp_workorder_produce_view.xml"
        ],
    "installable": True,
    "auto_install": True
}
