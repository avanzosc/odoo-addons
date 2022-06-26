# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Event Attendance Report Claim",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Custom",
    "license": "AGPL-3",
    "depends": [
        "event_attendance_report",
        "website_event_track_claim",
    ],
    "data": [
        "report/event_attendance_report_views.xml",
        "wizard/wiz_event_attendance_report_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
