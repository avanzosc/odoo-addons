# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Object Line Notes",
    "summary": "Customization Module",
    "version": "8.0.1.0.0",
    "category": "RGPD Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "sale",
        "purchase",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
        "views/account_invoice_views.xml",
        "views/account_invoice_line_views.xml",
        "views/stock_move_views.xml"
    ],
    "installable": True,
}
