# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Project User Product',
    'version': '8.0.1.0.0',
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        'Ana Juaristi <anajuaristi@avanzosc.es>',
        'Alfredo de la Fuente <alfredodelafuente@avanzosc.es',
    ],
    'category': 'Project Management',
    'depends': [
        'project_timesheet',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/project_project_view.xml",
        "views/project_user_product_view.xml",
    ],
    'installable': True,
}
