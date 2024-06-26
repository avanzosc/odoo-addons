# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Invoice Report Picking Info",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Invoices & Payments",
    "website": "http://www.avanzosc.es",
    "depends": [
        "web",
        "account",
        "sale",
        "stock",
        "sale_stock",
        "stock_picking_invoice_link",
    ],
    "data": [
        "reports/account_invoice_report.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
