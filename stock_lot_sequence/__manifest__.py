# -*- coding: utf-8 -*-
# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Lot Sequence",
    "summary": "Customization Module",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "stock",
    ],
    "data": [
    ],
    "installable": True,
    "post_init_hook": "_post_install_change_lot_sequence",
}
