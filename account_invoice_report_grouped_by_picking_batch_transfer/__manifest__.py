# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Report Grouped By Picking Batch Transfer",
    "version": "16.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account_invoice_report_grouped_by_picking", "stock_picking_batch"],
    "data": [
        "reports/account_invoice_reports.xml",
    ],
    "installable": True,
}
