# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Information Sale Forecast",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    'category': 'Warehouse Management',
    'depends': ['stock_information',
                'procurement_sale_forecast',
                ],
    "data": [
        "views/stock_information_view.xml",
        "views/procurement_sale_forecast_line_view.xml",
    ],
    'installable': True,
}
