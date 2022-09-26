# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Event Report",
    "version": "14.0.1.4.0",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Custom",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_with_start_end_date_period",
        "contract",
        "sale_order_line_contract",
        "event_sale",
        "event_registration_student",
        "event_registration_sale_line_contract"
    ],
    "data": [
        "views/account_move_views.xml",
        "views/sale_order_views.xml",
        "report/account_invoice_report.xml"
    ],
    "installable": True,
}
