# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Calendar School",
    "version": "12.0.1.3.0",
    "license": "AGPL-3",
    "depends": [
        "calendar",
        "hr_school",
        "crm",
        "contacts_school_education",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Extra Tools",
    "data": [
        "security/ir.model.access.csv",
        "data/calendar_school_data.xml",
        "views/hr_employee_supervised_year_view.xml",
        "views/calendar_event_view.xml",
        "views/hr_employee_view.xml",
        "views/res_partner_view.xml",
        "views/calendar_school_menu_view.xml",
        "wizard/wiz_generate_meeting_from_tutoring_view.xml",
        "wizard/wiz_change_teacher_calendar_event_view.xml",
    ],
    "installable": True,
}
