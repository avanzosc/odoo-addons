# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Sale Mrp Link",
    "version": "8.0.1.0.0",
    "category": "Sales Management",
    "license": "AGPL-3",
    "author": "OdooMRP team,"
              "AvanzOSC",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "mrp_production_sale_info",
        "sale_product_variants",
        "sale_mrp_project_link",
    ],
    "data": [
        "views/sale_view.xml",
        "views/mrp_view.xml",
    ],
    "installable": True,
}
