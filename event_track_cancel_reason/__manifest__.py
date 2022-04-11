# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Track Cancel Reason",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Sales/CRM",
    "depends": [
        "event_track_analytic",
        "hr_timesheet_time_type"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/event_track_cancel_reason_data.xml",
        "wizard/event_track_cancel_wizard_view.xml",
        "views/cancel_reason_views.xml",
        "views/event_track_views.xml",
        "views/project_time_type_views.xml",
        "views/account_analytic_line_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
