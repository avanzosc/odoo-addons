# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Picking With Analytic Account',
    'version': '11.0.1.1.1',
    'license': "AGPL-3",
    'summary': '''Stock picking with analytic account''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Accounting',
    'depends': [
        'analytic',
        'stock',
    ],
    'data': [
        "views/stock_picking_view.xml",
        "views/account_analytic_account_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
