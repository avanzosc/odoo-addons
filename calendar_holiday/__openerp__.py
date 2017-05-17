# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Calendar Holiday",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    "category": "Human Resources",
    "depends": [
        "mail",
        "hr_contract",
        "hr_holidays",
        "hr_employee_catch_partner",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/calendar_holiday_data.xml",
        "wizard/wiz_calculate_workable_festive_view.xml",
        "views/calendar_holiday_view.xml",
        "views/calendar_holiday_day_view.xml",
        "views/res_partner_calendar_view.xml",
        "views/res_partner_calendar_day_view.xml",
        "views/hr_employee_view.xml",
        "views/hr_contract_view.xml",
        "views/hr_holidays_view.xml",
    ],
    "installable": True,
}
