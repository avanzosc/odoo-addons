# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account Invoice Manual Analytic",
    "version": "8.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <ajuaristio@gmail.com>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "account",
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
}
