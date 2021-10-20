# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Track Analytic",
    'version': '14.0.1.4.0',
    "author": "Avanzosc",
    "category": "Marketing/Events",
    "depends": [
        "project",
        "analytic",
        "website_event_track",
        "hr_timesheet",
        "event_sale",
        "event_schedule",
        "sale_project",
        "sale_timesheet"
    ],
    "data": [
        "views/event_event_views.xml",
        "views/event_track_views.xml",
        "views/account_analytic_line_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
