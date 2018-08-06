# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "WMS Accounting Utilities",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Hidden",
    "depends": [
        "stock_account",
    ],
    "data": [
        "security/stock_account_security.xml",
        "views/res_config_view.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
