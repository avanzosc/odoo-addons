# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Price Shared",
    'version': '14.0.1.0.0',
    "category": "Marketing/Events",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "event",
        "event_sale",
        "website_event_track",
        "website_event_track_claim",
        "event_track_analytic",
        "sale_order_event_attendee"
    ],
    "data": [
        "views/event_event_views.xml",
        "views/event_registration_views.xml",
        "views/event_track_views.xml",
    ],
    'installable': True,
    'auto_install': False,
}
