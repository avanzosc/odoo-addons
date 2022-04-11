# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Track Cancel Billability",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Marketing/Events",
    "depends": [
        "event_track_cancel_reason",
    ],
    "data": [
        "views/event_track_views.xml",
        "views/event_event_views.xml",
        "wizard/event_track_cancel_wizard_view.xml",
        "views/account_analytic_line_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
