# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Customer Invoice Personalized Report",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Custom Module",
    "depends": [
        "report",
        "account",
        "account_invoice_line_stock_move_info"
    ],
    "data": [
        "report/report_customer_invoice_personalized.xml",
        "views/customer_invoice_personalized_report.xml",
    ],
    "installable": True,
}
