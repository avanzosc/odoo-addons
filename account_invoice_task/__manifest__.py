# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice with Project Task",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Accounting",
    "depends": [
        "account",
        "account_invoicing",
        "analytic",
        "hr_timesheet",
        "project",
    ],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/account_invoice_views.xml",
        "views/account_invoice_line_views.xml",
        "views/account_move_line_views.xml",
    ],
    "installable": True,
}
