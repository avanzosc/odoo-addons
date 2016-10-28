# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Quality Control By Product",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Quality control",
    "depends": [
        "quality_control_stock",
    ],
    "data": [
        "views/qc_test_view.xml",
        "views/product_view.xml",
        "views/partner_view.xml",
        "wizard/qc_test_wizard_view.xml"
    ],
    "installable": True,
}
