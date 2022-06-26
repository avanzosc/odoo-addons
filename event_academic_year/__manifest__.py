# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Academic Year",
    'version': '14.0.1.3.0',
    "category": "Marketing/Events",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "event",
        "website_event_track",
        "event_track_usability"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/event_academic_year_views.xml",
        "views/event_event_views.xml",
        "views/event_track_views.xml",
    ],
    'installable': True,
}
