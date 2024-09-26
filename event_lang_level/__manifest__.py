# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Lang Level",
    "version": "14.0.1.0.0",
    "category": "Marketing/Events",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "event_schedule",
        "event_create_track",
        "hr_skills",
    ],
    "data": [
        "views/hr_skill_type_views.xml",
        "views/hr_skill_views.xml",
        "views/event_event_views.xml",
        "views/event_track_views.xml",
    ],
    "installable": True,
}
