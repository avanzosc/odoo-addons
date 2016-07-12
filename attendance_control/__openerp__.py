# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Attendance Control",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "marketing",
        "mail",
        "hr_attendance_from_kanban",
        "hr_holidays",
        "hr_expense",
        "website",
    ],
    "data": [
        "data/res_user_data.xml",
        "security/attendance_security.xml",
        "views/menu_view.xml",
        "views/hr_view.xml",
    ],
    "installable": True,
}
