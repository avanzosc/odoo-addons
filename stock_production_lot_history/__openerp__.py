# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Production Lot History",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Warehouse Management",
    "depends": [
        "stock",
    ],
    "data": [
        "data/stock_production_lot_history_data.xml",
        "security/ir.model.access.csv",
        "wizard/wiz_change_lot_state_view.xml",
        "views/stock_production_lot_view.xml",
        "views/stock_quant_view.xml",
        "views/stock_production_lot_status_view.xml",
    ],
    "installable": True,
}
