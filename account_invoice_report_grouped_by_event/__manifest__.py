# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Report Grouped By Event",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Invoices & Payments",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_with_event_ticket",
        "account_invoice_with_start_end_date_period",
        "contract",
        "sale_order_line_contract",
        "event_sale",
        "event_registration_student",
        "event_registration_sale_line_contract",
    ],
    "data": ["report/account_invoice_report.xml", "views/res_partner_views.xml"],
    "installable": True,
}
