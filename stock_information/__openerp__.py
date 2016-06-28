# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock information",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    'category': 'Warehouse Management',
    'depends': ['sale',
                'purchase',
                'stock',
                'product_stock_info'
                ],
    'data': ['security/stock_information.xml',
             'security/ir.model.access.csv',
             'wizard/wiz_stock_information_view.xml',
             'wizard/wiz_create_procurement_stock_info_view.xml',
             'wizard/wiz_run_procurement_stock_info_view.xml',
             'views/procurement_order_view.xml',
             'views/stock_information_view.xml',
             ],
    'installable': True,
}
