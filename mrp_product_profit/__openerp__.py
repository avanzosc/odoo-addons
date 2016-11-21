# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Profit and Commercial on Schedule Products",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_mrp_link",
        "mrp_supplier_price",
        "mrp_routing_cost",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "category": "Manufacturing",
    "data": [
        "views/sale_view.xml",
        "views/mrp_production_view.xml",
        "views/res_config_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
