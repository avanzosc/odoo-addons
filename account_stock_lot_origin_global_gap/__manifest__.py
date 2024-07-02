# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Stock Lot Origin Global Gap",
    "version": "16.0.1.1.0",
    "category": "Invoices & Payments",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "sale_stock",
        "stock_account",
        "stock_lot_origin_global_gap",
        "stock_picking_invoice_link",
        "mrp",
        "account",
        "purchase",
    ],
    "data": [
        "report/report_invoice.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
}
