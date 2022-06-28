# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Komalingua Reports",
    "version": "14.0.1.2.0",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_event_report",
        "account_payment_partner",
        "hr_expense_event_commute",
        "event_attendance_report"
    ],
    "data": [
        "views/account_move_views.xml",
        "views/res_company_views.xml",
        "report/report_layout.xml",
        "report/account_invoice_report.xml",
        "report/event_attendance_report_views.xml"
    ],
    "installable": True,
}
