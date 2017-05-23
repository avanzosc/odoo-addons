# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Hr Attendance Report",
    "version": "8.0.1.0.0",
    "category": "Human Resources",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "hr_attendance",
        "hr_timesheet_sheet",
    ],
    "data": [
        "report/attendance_report.xml",
        "report/hr_layout.xml",
    ],
    "installable": True,
}
