# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event Registration Analytic",
    'version': '8.0.1.1.0',
    'license': "AGPL-3",
    'author': "AvanzOSC",
    'website': "http://www.avanzosc.es",
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    "category": "Event Management",
    "depends": [
        'analytic',
        'account_analytic_analysis',
        'event_sale',
        'sale_order_create_event'
    ],
    "data": [
        'wizard/wiz_event_append_assistant_view.xml',
        'views/event_event_view.xml',
        'views/event_registration_view.xml',
        'views/sale_order_view.xml',
    ],
    "installable": True,
}
