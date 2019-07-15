# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Purchase Requisition From Sale Order',
    'version': '8.0.1.0.0',
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        'Ana Juaristi <anajuaristi@avanzosc.es>',
        'Alfredo de la Fuente <alfredodelafuente@avanzosc.es',
    ],
    'category': 'Sales Management',
    'depends': [
        'sale',
        'purchase_requisition'
    ],
    'data': [
        "views/sale_order_view.xml",
        "views/purchase_requision_view.xml",
    ],
    'installable': True,
}
