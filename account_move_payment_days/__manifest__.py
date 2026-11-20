# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Move Payment Days Analysis",
    "summary": "Supplier payment days by payment mode, with average pivot analysis",
    "version": "18.0.1.0.0",
    "category": "Accounting/Accounting",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "account_payment_partner",
        "account_invoice_date_due",
        "partner_time_to_pay",
    ],
    "data": [
        "views/account_payment_mode_view.xml",
        "views/account_move_view.xml",
        "views/account_invoice_report_view.xml",
    ],
    "installable": True,
    "application": False,
}
