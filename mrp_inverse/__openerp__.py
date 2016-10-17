# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "MRP Production Inverse",
    "summary": "Ability to create a inverse productions.",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "http://www.avanzosc.es/",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'mrp',
    ],
    "data": [
        "views/mrp_bom_view.xml",
        "wizards/inverse_mrp_product_produce_view.xml",
        "views/mrp_production_view.xml",
    ],
}
