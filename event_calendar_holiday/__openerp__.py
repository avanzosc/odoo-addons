# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event Calendar Holiday",
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
        'calendar_holiday',
        'sale_order_create_event'
    ],
    "data": [
        'views/account_analytic_account_view.xml',
        'views/event_track_presence_view.xml',
        'views/res_partner_calendar_day_view.xml',
        'views/event_track_view.xml'
    ],
    "installable": True,
}
