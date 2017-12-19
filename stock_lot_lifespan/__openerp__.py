# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Lot Lifespan",
    "version": "8.0.1.0.0",
    "category": "Warehouse Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "product_expiry_ext",
    ],
    "post_init_hook": "load_alert_dates",
    "data": [
        "data/stock_lot_lifespan.xml",
        "views/res_config_view.xml",
        "views/stock_production_lot_view.xml",
    ],
    "installable": True,
}
