# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Stock Information MRP Procurement Plan',
    "version": "8.0.1.0.0",
    "license": 'AGPL-3',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    'category': 'Warehouse Management',
    'depends': ['procurement_plan_mrp',
                'stock_information_mrp',
                ],
    'data': ['views/stock_information_view.xml',
             'views/procurement_plan_view.xml',
             ],
    'installable': True,
    'auto_install': True,
}
