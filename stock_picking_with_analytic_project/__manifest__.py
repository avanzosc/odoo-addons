# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Picking With Analytic Project',
    'version': '11.0.1.0.0',
    'license': "AGPL-3",
    'summary': '''Stock picking with analytic project''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Accounting',
    'depends': [
        'stock_picking_with_analytic_account',
        'project',
    ],
    'data': [
        "views/project_project_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
