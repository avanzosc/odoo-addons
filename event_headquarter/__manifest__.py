# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Headquarter",
    'version': '14.0.1.0.0',
    "category": "Marketing/Events",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "res_partner_headquarter",
        "event",
        "event_track_analytic"
    ],
    "data": [
        "views/event_event_views.xml",
        "views/account_analytic_line_views.xml",
    ],
    'installable': True,
}
