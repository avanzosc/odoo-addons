# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event Attendance Report",
    "version": "14.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "event",
        "event_registration_student",
        "website_event_track",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/event_attendance_report_data.xml",
        "wizard/wiz_event_attendance_report_views.xml",
        "report/event_attendance_report_views.xml",
    ],
    "installable": True,
}
