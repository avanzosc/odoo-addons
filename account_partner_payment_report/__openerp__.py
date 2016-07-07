# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account Partner Payment Report",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es",
    ],
    "category": "Accounting & Finance",
    "depends": [
        "account_financial_report_webkit",
        "account_due_list_payment_mode"
    ],
    "data": [
        "report/report.xml",
        "wizard/report_partner_payment_view.xml",
    ],
    "installable": True,
}
