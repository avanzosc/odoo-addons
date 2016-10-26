# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Account Invoice Partner Bank",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Accounting & Finance",
    "depends": [
        "account_payment",
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/payment_mode_view.xml"
    ],
    "installable": True,
}
