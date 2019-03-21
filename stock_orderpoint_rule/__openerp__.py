# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Orderpoint Rule",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Warehouse Management",
    "depends": ['sale',
                'purchase',
                'stock',
                ],
    "data": [
        "views/res_company_view.xml",
        "views/stock_planning_view.xml",
        "wizard/orderpoint_procurement_view.xml",
        "data/cron.xml"
    ],
    "installable": True,
}
