# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Lot Invoicing",
    "summary": "",
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
        "stock_account",
    ],
    "data": [
        "views/stock_production_lot_view.xml",
        "wizard/stock_transfer_details_view.xml"
    ],
    "installable": True,
}
