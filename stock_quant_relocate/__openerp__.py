# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Quant Relocate",
    "version": "8.0.0.1.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Warehouse Management",
    "depends": [
        "stock_quant_packages_moving_wizard",
    ],
    "data": [
        "wizard/quant_move_wizard_view.xml",
        "views/product_category_view.xml",
        "views/product_template_view.xml",
        "views/stock_picking_type_view.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
