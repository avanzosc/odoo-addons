# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Report GDPR",
    "summary": "Customization Module",
    "version": "8.0.1.0.0",
    "category": "GDPR Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "sale",
        "purchase",
    ],
    "data": [
        "report/sale_order_report.xml",
        "report/purchase_order_report.xml",
        "report/account_invoice_report.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
}
