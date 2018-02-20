# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account Invoice Supplier Validation",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Accounting & Finance",
    "depends": [
        "hr",
        "stock_account",
        "purchase",
        "account_cancel",
    ],
    "data": [
        "workflow/account_invoice.xml",
        "views/account_invoice_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
